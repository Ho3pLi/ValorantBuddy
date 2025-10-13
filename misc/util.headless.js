import https from "https";
import http from "http";
import fs from "fs";
import config from "./config.js";

// Lightweight fetch with TLS settings (copied from util.js)
const tlsCiphers = [
  'TLS_CHACHA20_POLY1305_SHA256', 'TLS_AES_128_GCM_SHA256', 'TLS_AES_256_GCM_SHA384',
  'ECDHE-ECDSA-CHACHA20-POLY1305', 'ECDHE-RSA-CHACHA20-POLY1305', 'ECDHE-ECDSA-AES128-SHA256',
  'ECDHE-RSA-AES128-SHA256', 'ECDHE-ECDSA-AES256-GCM-SHA384', 'ECDHE-RSA-AES256-GCM-SHA384',
  'ECDHE-ECDSA-AES128-SHA', 'ECDHE-RSA-AES128-SHA', 'ECDHE-ECDSA-AES256-SHA', 'ECDHE-RSA-AES256-SHA',
  'RSA-PSK-AES128-GCM-SHA256', 'RSA-PSK-AES256-GCM-SHA384', 'RSA-PSK-AES128-CBC-SHA', 'RSA-PSK-AES256-CBC-SHA'
];
const tlsSigAlgs = [
  'ecdsa_secp256r1_sha256','rsa_pss_rsae_sha256','rsa_pkcs1_sha256','ecdsa_secp384r1_sha384',
  'rsa_pss_rsae_sha384','rsa_pkcs1_sha384','rsa_pss_rsae_sha512','rsa_pkcs1_sha512','rsa_pkcs1_sha1'
];

export const fetch = (url, options = {}) => {
  if (config.logUrls) console.log("Fetching url " + url.substring(0, 200) + (url.length > 200 ? "..." : ""));
  return new Promise((resolve, reject) => {
    const req = https.request(url, {
      agent: options.proxy,
      method: options.method || "GET",
      headers: {
        cookie: "dummy=cookie",
        "Accept-Language": "en-US,en;q=0.5",
        referer: "https://github.com/giorgi-o/SkinPeek",
        ...options.headers,
      },
      ciphers: tlsCiphers.join(':'),
      sigalgs: tlsSigAlgs.join(':'),
      minVersion: "TLSv1.3",
    }, (resp) => {
      const res = { statusCode: resp.statusCode, headers: resp.headers };
      const chunks = [];
      resp.on('data', (c) => chunks.push(c));
      resp.on('end', () => {
        res.body = Buffer.concat(chunks).toString(options.encoding || "utf8");
        resolve(res);
      });
      resp.on('error', (err) => { console.error(err); reject(err); });
    });
    req.write(options.body || "");
    req.end();
    req.on('error', (err) => { console.error(err); reject(err); });
  });
};

// Proxy manager (HTTPS only)
const ProxyType = { HTTPS: "https" };
class Proxy {
  constructor({ manager, type, host, port, username, password }) {
    this.manager = manager; this.type = type || ProxyType.HTTPS;
    this.host = host; this.port = port; this.username = username; this.password = password;
  }
  createAgent(hostname) {
    if (this.type !== ProxyType.HTTPS) throw new Error("Unsupported proxy type " + this.type);
    return new Promise((resolve, reject) => {
      const headers = { "User-Agent": "Mozilla/5.0", Host: hostname };
      if (this.username && this.password) {
        headers["Proxy-Authorization"] = "Basic " + Buffer.from(`${this.username}:${this.password}`).toString("base64");
      }
      const req = http.request({ host: this.host, port: this.port, method: "CONNECT", path: hostname + ":443", headers });
      req.on("connect", (_res, socket) => { resolve(new https.Agent({ socket })); });
      req.on("error", (err) => reject(`Proxy ${this.host}:${this.port} errored: ${err}`));
      req.end();
    });
  }
}
class ProxyManager {
  constructor() { this.allProxies = []; this.enabled = false; }
  async loadProxies() {
    try {
      const text = fs.readFileSync("data/proxies.txt", "utf8");
      for (const line of text.split("\n")) {
        const trimmed = line.trim(); if (!trimmed || trimmed.startsWith('#')) continue;
        const [host, portStr, type, username, password] = trimmed.split(":");
        const port = parseInt(portStr); if (!host || isNaN(port)) continue;
        this.allProxies.push(new Proxy({ manager: this, type: type || ProxyType.HTTPS, host, port, username, password }));
      }
      this.enabled = this.allProxies.length > 0;
    } catch (_) { /* no proxies file */ }
  }
  async getProxy(hostname) {
    if (!this.enabled) return null;
    const p = this.allProxies[Math.floor(Math.random() * this.allProxies.length)];
    return p || null;
  }
}
let proxyManager = null;
export const initProxyManager = async () => {
  proxyManager = new ProxyManager();
  await proxyManager.loadProxies();
  return proxyManager;
};
export const getProxyManager = () => proxyManager || { enabled: false, getProxy: async () => null };

// Riot client headers and version
let riotVersionData = null;
export const getRiotVersionData = () => riotVersionData;
export const fetchRiotVersionData = async () => {
  try {
    const req = await fetch("https://valorant-api.com/v1/version");
    if (req.statusCode !== 200) return null;
    const json = JSON.parse(req.body);
    riotVersionData = json.data;
    return riotVersionData;
  } catch (e) { console.error(e); return null; }
};
const platformOsVersion = "10.0.19042.1.256.64bit";
export const riotClientHeaders = () => {
  const clientPlatformData = {
    platformType: "PC", platformOS: "Windows", platformOSVersion: platformOsVersion, platformChipset: "Unknown",
  };
  const clientPlatformDataJson = JSON.stringify(clientPlatformData, null, "\t");
  const clientPlatformDataBase64 = Buffer.from(clientPlatformDataJson.replace(/\n/g, "\r\n")).toString("base64");
  return {
    "X-Riot-ClientPlatform": clientPlatformDataBase64,
    "X-Riot-ClientVersion": riotVersionData?.riotClientVersion || "",
  };
};

// Auth helpers
export const parseSetCookie = (setCookie) => {
  if (!setCookie) return {};
  const cookies = {};
  for (const cookie of setCookie) {
    const sep = cookie.indexOf("=");
    cookies[cookie.slice(0, sep)] = cookie.slice(sep + 1, cookie.indexOf(';'));
  }
  return cookies;
};
export const stringifyCookies = (cookies) => Object.entries(cookies).map(([k, v]) => `${k}=${v}`).join("; ");
export const extractTokensFromUri = (uri) => {
  const match = uri.match(/access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)/);
  if (!match) return [null, null];
  const [, accessToken, idToken] = match; return [accessToken, idToken];
};
export const decodeToken = (token) => JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString('utf8'));
export const tokenExpiry = (token) => decodeToken(token).exp * 1000;

// Misc helpers
export const userRegion = ({ region }) => (!region || region === "latam" || region === "br") ? "na" : region;
export const isMaintenance = (json) => json.httpStatus === 403 && json.errorCode === "SCHEDULED_DOWNTIME";
export const ensureUsersFolder = () => { if (!fs.existsSync("data")) fs.mkdirSync("data"); if (!fs.existsSync("data/users")) fs.mkdirSync("data/users"); };
export const wait = (ms) => new Promise((r) => setTimeout(r, ms));
export const isSameDay = (t1, t2) => { t1 = new Date(t1); t2 = new Date(t2); return t1.getUTCFullYear() === t2.getUTCFullYear() && t1.getUTCMonth() === t2.getUTCMonth() && t1.getUTCDate() === t2.getUTCDate(); };

// Formatting helpers used by shop
export const formatBundle = async (rawBundle) => {
  const bundle = { uuid: rawBundle.DataAssetID, expires: Math.floor(Date.now() / 1000) + rawBundle.DurationRemainingInSeconds, items: [] };
  let price = 0, basePrice = 0;
  for (const rawItem of rawBundle.Items) {
    const item = {
      uuid: rawItem.Item.ItemID,
      type: rawItem.Item.ItemTypeID,
      amount: rawItem.Item.Amount,
      price: rawItem.DiscountedPrice,
      basePrice: rawItem.BasePrice,
      discount: rawItem.DiscountPercent,
    };
    price += item.price; basePrice += item.basePrice; bundle.items.push(item);
  }
  bundle.price = price; bundle.basePrice = basePrice; return bundle;
};

export const formatNightMarket = (rawNightMarket) => {
  if (!rawNightMarket) return null;
  return {
    offers: rawNightMarket.BonusStoreOffers.map(offer => ({
      uuid: offer.Offer.OfferID,
      realPrice: offer.Offer.Cost["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
      nmPrice: offer.DiscountCosts["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
      percent: offer.DiscountPercent,
    })),
    expires: Math.floor(Date.now() / 1000) + rawNightMarket.BonusStoreRemainingDurationInSeconds,
  };
};
