import { authUser, deleteUserAuth, getUser } from "../valorant/auth.js";
import { fetch, userRegion, riotClientHeaders, isMaintenance, formatNightMarket } from "../misc/util.headless.js";

export const getShopRaw = async (id, account = null) => {
  const authSuccess = await authUser(id, account);
  if (!authSuccess.success) return authSuccess;

  const user = getUser(id, account);
  const req = await fetch(`https://pd.${userRegion(user)}.a.pvp.net/store/v3/storefront/${user.puuid}`, {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + user.auth.rso,
      "X-Riot-Entitlements-JWT": user.auth.ent,
      ...riotClientHeaders(),
    },
    body: JSON.stringify({})
  });

  if (req.statusCode !== 200) return { success: false };
  const json = JSON.parse(req.body);
  if (json.httpStatus === 400 && json.errorCode === "BAD_CLAIMS") {
    deleteUserAuth(user);
    return { success: false };
  } else if (isMaintenance(json)) return { success: false, maintenance: true };
  return { success: true, shop: json };
};

export const getOffersApi = async (id, account = null) => {
  const resp = await getShopRaw(id, account);
  if (!resp.success) return resp;

  return {
    success: true,
    offers: resp.shop.SkinsPanelLayout.SingleItemOffers,
    expires: Math.floor(Date.now() / 1000) + resp.shop.SkinsPanelLayout.SingleItemOffersRemainingDurationInSeconds,
    accessory: {
      offers: (resp.shop.AccessoryStore.AccessoryStoreOffers || []).map(rawAccessory => ({
        cost: rawAccessory.Offer.Cost["85ca954a-41f2-ce94-9b45-8ca3dd39a00d"],
        rewards: rawAccessory.Offer.Rewards,
        contractID: rawAccessory.ContractID,
      })),
      expires: Math.floor(Date.now() / 1000) + resp.shop.AccessoryStore.AccessoryStoreRemainingDurationInSeconds,
    },
  };
};

export const getBundlesApi = async (id, account = null) => {
  const resp = await getShopRaw(id, account);
  if (!resp.success) return resp;
  const now = Math.floor(Date.now() / 1000);
  const bundles = resp.shop.FeaturedBundle.Bundles.map(b => ({
    uuid: b.DataAssetID,
    expires: now + b.DurationRemainingInSeconds,
    items: b.Items?.length || 0,
  }));
  return { success: true, bundles };
};

export const getNightMarketApi = async (id, account = null) => {
  const resp = await getShopRaw(id, account);
  if (!resp.success) return resp;
  if (!resp.shop.BonusStore) return { success: true, offers: false };
  return { success: true, ...formatNightMarket(resp.shop.BonusStore) };
};

export const getBalanceApi = async (id, account = null) => {
  const authSuccess = await authUser(id, account);
  if (!authSuccess.success) return authSuccess;

  const user = getUser(id, account);
  const req = await fetch(`https://pd.${userRegion(user)}.a.pvp.net/store/v1/wallet/${user.puuid}`, {
    headers: {
      "Authorization": "Bearer " + user.auth.rso,
      "X-Riot-Entitlements-JWT": user.auth.ent,
      ...riotClientHeaders(),
    }
  });
  if (req.statusCode !== 200) return { success: false };
  const json = JSON.parse(req.body);
  if (json.httpStatus === 400 && json.errorCode === "BAD_CLAIMS") return { success: false };
  else if (isMaintenance(json)) return { success: false, maintenance: true };
  return {
    success: true,
    vp: json.Balances["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
    rad: json.Balances["e59aa87c-4cbf-517a-5983-6e81511be9b7"],
    kc: json.Balances["85ca954a-41f2-ce94-9b45-8ca3dd39a00d"],
  };
};

