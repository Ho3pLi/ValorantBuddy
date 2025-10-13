import express from "express";
import cors from "cors";

// Valorant modules reused from the bot
import { getUser, redeemUsernamePassword, redeem2FACode, redeemCookies } from "../valorant/auth.js";
import { getOffersApi, getBundlesApi, getNightMarketApi, getBalanceApi } from "./shopApi.js";
import { getLoadout, getSkins } from "../valorant/inventory.js";
import { fetchRiotVersionData, initProxyManager } from "../misc/util.headless.js";

const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Helper to extract client id and optional account index (1-based)
const getContext = (req) => {
  const id = req.header("x-client-id") || req.query.id;
  const account = req.header("x-account") || req.query.account;
  const accountNum = account ? parseInt(account) : null; // 1-based expected
  return { id, account: Number.isNaN(accountNum) ? null : accountNum };
};

const requireClientId = (req, res, next) => {
  const { id } = getContext(req);
  if (!id) return res.status(400).json({ success: false, error: "missing x-client-id" });
  next();
};

app.get("/health", (_req, res) => {
  res.json({ ok: true, name: "ValorantBuddy API" });
});

// Auth endpoints
app.post("/auth/login", requireClientId, async (req, res) => {
  try {
    const { id } = getContext(req);
    const { login, password } = req.body || {};
    if (!login || !password) return res.status(400).json({ success: false, error: "missing login/password" });
    const resp = await redeemUsernamePassword(id, login, password);
    return res.json(resp);
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "auth.login_failed" });
  }
});

app.post("/auth/2fa", requireClientId, async (req, res) => {
  try {
    const { id } = getContext(req);
    const { code } = req.body || {};
    if (!code) return res.status(400).json({ success: false, error: "missing 2fa code" });
    const resp = await redeem2FACode(id, code);
    return res.json(resp);
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "auth.2fa_failed" });
  }
});

app.post("/auth/cookies", requireClientId, async (req, res) => {
  try {
    const { id } = getContext(req);
    const { cookies } = req.body || {};
    if (!cookies) return res.status(400).json({ success: false, error: "missing cookies" });
    const resp = await redeemCookies(id, cookies);
    return res.json(resp);
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "auth.cookies_failed" });
  }
});

// Current account info
app.get("/users/me", requireClientId, (req, res) => {
  try {
    const { id, account } = getContext(req);
    const user = getUser(id, account);
    if (!user) return res.status(404).json({ success: false, error: "user_not_found" });
    const { puuid, username, region } = user;
    return res.json({ success: true, id, account: account || 1, puuid, username, region });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "users.me_failed" });
  }
});

// Shop endpoints
app.get("/shop/offers", requireClientId, async (req, res) => {
  try {
    const { id, account } = getContext(req);
    const resp = await getOffersApi(id, account);
    return res.json(resp);
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "shop.offers_failed" });
  }
});

app.get("/shop/bundles", requireClientId, async (req, res) => {
  try {
    const { id, account } = getContext(req);
    const resp = await getBundlesApi(id, account);
    return res.json(resp);
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "shop.bundles_failed" });
  }
});

app.get("/shop/nightmarket", requireClientId, async (req, res) => {
  try {
    const { id, account } = getContext(req);
    const resp = await getNightMarketApi(id, account);
    return res.json(resp);
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "shop.nightmarket_failed" });
  }
});

// Wallet
app.get("/wallet", requireClientId, async (req, res) => {
  try {
    const { id, account } = getContext(req);
    const resp = await getBalanceApi(id, account);
    return res.json(resp);
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "wallet.failed" });
  }
});

// Inventory
app.get("/inventory/loadout", requireClientId, async (req, res) => {
  try {
    const { id, account } = getContext(req);
    const user = getUser(id, account);
    if (!user) return res.status(404).json({ success: false, error: "user_not_found" });
    const resp = await getLoadout(user, account);
    return res.json(resp);
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "inventory.loadout_failed" });
  }
});

app.get("/inventory/skins", requireClientId, async (req, res) => {
  try {
    const { id, account } = getContext(req);
    const user = getUser(id, account);
    if (!user) return res.status(404).json({ success: false, error: "user_not_found" });
    const resp = await getSkins(user);
    return res.json(resp);
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, error: "inventory.skins_failed" });
  }
});

// Initialize helpers on startup
(async () => {
  await initProxyManager().catch(() => {});
  await fetchRiotVersionData().catch(() => {});
  app.listen(port, () => {
    console.log(`ValorantBuddy API listening on http://localhost:${port}`);
  });
})();
