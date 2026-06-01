// Archipelago client for Yarimono.

(function () {
    'use strict';
    // Global AP client instance, initialized on new game or load if save is marked as AP save.
    // If it's initialized AP specific logic will run, otherwise normal game logic will run.
    let client = null;

    // #region Constants
    const GAME = "Yarimono";
    const AP_VERSION = { major: 0, minor: 6, build: 7, class: "Version" };
    const ITEMS_HANDLING_ALL = 0b111; // remote + starting + self
    const CONNECT_TIMEOUT_MS = 7000;
    const AUTH_TIMEOUT_MS = 7000;
    const RECONNECT_DELAYS_MS = [1000, 2000, 4000, 8000, 16000];
    const DEFAULT_PORT = 38281;

    const ITEM_IDS = {
        BASE: 1082000,
        EVENT: 1083000,
        JUNK: 1084000,
        ULTIMATE_MOVE: 1085000,
        SCENE_UNLOCK: 1086000,
    }

    const LOCATION_IDS = {
        BASE: 1082000,
        TRAINER_FIGHT: 1082000,
        LEVEL_GRANT: 1083000,
        EXTRA_SHOP: 1084000,
        PICKUP: 1085000,
        SCENE_UNLOCK: 1086000,
        EVENT_PURCHASE: 1087000,
        EVENT_PICKUP: 1088000,
        STORY_CHECKPOINT: 1089000,
        ULTIMATE_MOVE: 1090000,
    }

    const CLIENT_GOAL = 30;

    const OPENING_CUTSCENE_MAP_ID = 3; // The map ID of the opening cutscene.
    const MENU_MAP_ID = 9; // The map ID of the main menu.
    const BATTLE_SYSTEM_MAP_ID = 31; // The map ID of the battle system where trainer fights happen.

    const SWITCH_ULTIMATE_MOVE_START = 42; // The ID of the first switch corresponding to an ultimate move unlock.
    const SWITCH_ULTIMATE_COUNT = 7; // The number of switches corresponding to ultimate move unlocks.

    const LEO_BIG_CITY_LOC_ID = LOCATION_IDS.TRAINER_FIGHT + 12 // Leo fight grants a level on loss as well as victory.

    const MENS_BATH_LEVEL_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 20
    const JIZO_SET_COMPLETE_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 30

    const MUSHROOM_LEVEL_HAJIME_ROAD_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 0;
    const MUSHROOM_LEVEL_CITY_ROAD_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 1;
    const MUSHROOM_LEVEL_WANO_VILLAGE_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 2;
    const MUSHROOM_LEVEL_HARBOR_TOWN_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 3;
    const MUSHROOM_LEVEL_CENTRAL_ROAD_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 4;
    const MUSHROOM_LEVEL_LAVA_HIDEOUT_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 5;
    const MUSHROOM_LEVEL_INLET_HIDEOUT_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 6;
    const MUSHROOM_LEVEL_FOREST_HIDEOUT_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 7;
    const MUSHROOM_LEVEL_SECRET_SHOP_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 10;

    const MUSHROOM_LOCATIONS = [
        MUSHROOM_LEVEL_HAJIME_ROAD_LOC_ID,
        MUSHROOM_LEVEL_CITY_ROAD_LOC_ID,
        MUSHROOM_LEVEL_WANO_VILLAGE_LOC_ID,
        MUSHROOM_LEVEL_HARBOR_TOWN_LOC_ID,
        MUSHROOM_LEVEL_CENTRAL_ROAD_LOC_ID,
        MUSHROOM_LEVEL_LAVA_HIDEOUT_LOC_ID,
        MUSHROOM_LEVEL_INLET_HIDEOUT_LOC_ID,
        MUSHROOM_LEVEL_FOREST_HIDEOUT_LOC_ID,
        MUSHROOM_LEVEL_SECRET_SHOP_LOC_ID,
    ];


    const PICKUP_CHEST_BIG_CITY_STAR_DISK_LOC_ID   = LOCATION_IDS.PICKUP +  0;
    const PICKUP_CHEST_BIG_CITY_CASTELLA_LOC_ID    = LOCATION_IDS.PICKUP +  1;
    const PICKUP_HIDDEN_BIG_CITY_5000_LOC_ID       = LOCATION_IDS.PICKUP +  2;
    const PICKUP_CHEST_HAJIME_ROAD_LOC_ID          = LOCATION_IDS.PICKUP +  3;
    const PICKUP_CHEST_CAVE_ROAD_LOC_ID            = LOCATION_IDS.PICKUP +  4;
    const PICKUP_CHEST_WANO_CAVE_1F_ATTACK_LOC_ID  = LOCATION_IDS.PICKUP +  5;
    const PICKUP_CHEST_WANO_CAVE_1F_SOUP_LOC_ID    = LOCATION_IDS.PICKUP +  6;
    const PICKUP_CHEST_WANO_CAVE_1F_CASTLA_LOC_ID  = LOCATION_IDS.PICKUP +  7;
    const PICKUP_CHEST_WANO_CAVE_B1F_SOUP_LOC_ID   = LOCATION_IDS.PICKUP +  8;
    const PICKUP_HIDDEN_HARBOR_TOWN_5000_LOC_ID    = LOCATION_IDS.PICKUP +  9;
    const PICKUP_CHEST_HARBOR_TOWN_MUSHROOM_LOC_ID = LOCATION_IDS.PICKUP + 10;
    const PICKUP_CHEST_HARBOR_TOWN_SOUP_LOC_ID     = LOCATION_IDS.PICKUP + 11;
    const PICKUP_CHEST_CENTRAL_ROAD_SOUP_LOC_ID    = LOCATION_IDS.PICKUP + 12;
    const PICKUP_HIDDEN_BASEMENT_INCENSE_LOC_ID    = LOCATION_IDS.PICKUP + 13;
    const PICKUP_HIDDEN_BASEMENT_DETERGENT_LOC_ID  = LOCATION_IDS.PICKUP + 14;
    const PICKUP_CHEST_HOLY_ROAD_LOC_ID            = LOCATION_IDS.PICKUP + 15;
    const PICKUP_CHEST_CONSTRUCTION_OFFICE_LOC_ID  = LOCATION_IDS.PICKUP + 16;
    const PICKUP_CHEST_SAND_AREA_1_LOC_ID          = LOCATION_IDS.PICKUP + 17;
    const PICKUP_CHEST_SAND_AREA_2_LOC_ID          = LOCATION_IDS.PICKUP + 18;
    const PICKUP_CHEST_COASTLINE_LOC_ID            = LOCATION_IDS.PICKUP + 19;

    const ED_SETUP_LEVEL_1_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 40;
    const ED_SETUP_LEVEL_2_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 41;
    const ED_SETUP_LEVEL_3_LOC_ID = LOCATION_IDS.LEVEL_GRANT + 42;

    const VIP_CARD_LOC_ID = LOCATION_IDS.EVENT_PICKUP + 31;

    const EVENT_SHOP_ITEM_IDS = [50, 51, 52, 54, 41, 42, 43, 44, 45, 46, 47, 53, 56, 57, 38, 39];

    const TEXT_BOX_CHAR_LIMIT = 55;

    const GOAL_TRAINER_IDS = {
        0: 80,
        1: 77,
        2: 217,
        3: 221,
    }

    const DREAM_SWITCHES = {
        DREAM_1: 99,
        DREAM_2: 105,
        DREAM_3: 115,
        DREAM_4: 121,
    }

    const DREAM_SWITCH_SET = new Set(Object.values(DREAM_SWITCHES));

    const DREAM_LOC_IDS = {
        DREAM_1: LOCATION_IDS.STORY_CHECKPOINT + 2,
        DREAM_2: LOCATION_IDS.STORY_CHECKPOINT + 3,
        DREAM_3: LOCATION_IDS.STORY_CHECKPOINT + 4,
        DREAM_4: LOCATION_IDS.STORY_CHECKPOINT + 5,
    }

    const SECRET_SHOP_MATSUTAKE_LOC_ID = LOCATION_IDS.EVENT_PURCHASE + 56;
    const SECRET_SHOP_WONDERFUL_SPRAY_LOC_ID = LOCATION_IDS.EVENT_PURCHASE + 57;
    const SECRET_SHOP_NOSE_HOOK_LOC_ID = LOCATION_IDS.EVENT_PURCHASE + 47;
    const SECRET_SHOP_STRANGE_MEDICINE_LOC_ID = LOCATION_IDS.EVENT_PURCHASE + 42;

    const EVENT_SHOP_ITEM_ID_BASE = 100; // Items to replace event items normally sold in shops. 
    const AP_SHOP_ITEM_ID_BASE = 200; // Items to add to shops for extra levels.

    const TOTORO_SCENE_2_LOC_ID = LOCATION_IDS.SCENE_UNLOCK + 311;

    const trainerRecLevelAdjustments = [
        { id: 140, name: 'Hotaru', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 142, name: 'Sanae', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 144, name: 'Maho', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 145, name: 'Kuina', suisyoLv: 150, trLvHikakuMinLv: 100 },
        { id: 147, name: 'Honoka', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 151, name: 'Melon', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 152, name: 'Riona', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 155, name: 'Yoru and Neru ', suisyoLv: 120, trLvHikakuMinLv: 120 },
        { id: 156, name: 'Maki', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 157, name: 'Murasaki', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 163, name: 'Nene', suisyoLv: 110, trLvHikakuMinLv: 110 },
        { id: 165, name: 'Marisa', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 167, name: 'Rumi', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 173, name: 'Taiga', suisyoLv: 120, trLvHikakuMinLv: 120 },
        { id: 174, name: 'Minako', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 182, name: 'Akira', suisyoLv: 120, trLvHikakuMinLv: 120 },
        { id: 183, name: 'Kanako', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 193, name: 'Nanase', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 200, name: 'Murei', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 201, name: 'Aya', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 204, name: 'Hikari', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 205, name: 'Leo', suisyoLv: 100, trLvHikakuMinLv: 100 },
        { id: 207, name: 'Lisa', suisyoLv: 110  , trLvHikakuMinLv: 110 },
        { id: 208, name: 'Sophia', suisyoLv: 110, trLvHikakuMinLv: 110 },
        { id: 209, name: 'Hiroko ', suisyoLv: 110, trLvHikakuMinLv: 110 },
        { id: 210, name: 'Hibana', suisyoLv: 110, trLvHikakuMinLv: 110 },
        { id: 211, name: 'Ero-doujin Sensei', suisyoLv: 120, trLvHikakuMinLv: 120 },
        { id: 212, name: 'Meena', suisyoLv: 110, trLvHikakuMinLv: 110 },
        { id: 213, name: 'Shishio', suisyoLv: 110, trLvHikakuMinLv: 110 },
        { id: 214, name: 'Anna', suisyoLv: 110, trLvHikakuMinLv: 110 },
        { id: 221, name: 'Nupuryu', suisyoLv: 140, trLvHikakuMinLv: 140 }
    ]
    // #endregion

    // #region CSS 
    const Z_INDEX = { blocker: 9998, modal: 10000, toast: 10100 };

    const STYLE_TAG_ID = 'yarimono-styles';
    const STYLE_CSS = `
.blocker {
    position: fixed; inset: 0;
    z-index: ${Z_INDEX.blocker};
    background: transparent;
    pointer-events: auto;
}
.modal {
    position: fixed;
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    z-index: ${Z_INDEX.modal};
    display: flex; align-items: center; justify-content: center;
    background: transparent;
    font: 13px/1.35 Consolas, monospace;
    color: #fff;
    text-shadow: 1px 1px 2px #000, 0 0 4px #000;
}
.card {
    min-width: 320px;
    background: rgba(0,0,0,0.9);
    padding: 8px 12px;
}
.card h2 {
    margin: 0 0 8px;
    font: inherit;
    font-weight: bold;
    color: #38d5ea;
}
.field {
    display: flex; flex-direction: column;
    margin-bottom: 6px;
}
.field label {
    color: #ccc;
    margin-bottom: 2px;
}
.field input {
    background: rgba(0,0,0,0.6);
    border: 1px solid #38d5ea;
    padding: 2px 4px;
    color: #fff;
    font: inherit;
    text-shadow: inherit;
    outline: none;
}
.field input:focus { border-color: #fbb96a; }
.actions { margin-top: 8px; display: flex; justify-content: flex-end; width: 100%; }
.btn {
    background: rgba(0,0,0,0.6);
    color: #fff;
    border: 1px solid #38d5ea;
    padding: 2px 12px;
    font: inherit;
    text-shadow: inherit;
    cursor: pointer;
}
.btn:hover { border-color: #fbb96a; color: #fbb96a; }
.btn:focus { border-color: #fbb96a; outline: none; }
.toast-container {
    position: fixed;
    top: 8px; right: 8px;
    z-index: ${Z_INDEX.toast};
    display: flex; flex-direction: column;
    gap: 2px;
    align-items: flex-end;
    pointer-events: none;
    max-width: 480px;
}
.toast {
    background: rgba(0,0,0,0.6);
    color: #fff;
    border-left: 4px solid #38d5ea;
    padding: 3px 8px;
    font: 13px/1.35 Consolas, monospace;
    text-shadow: 1px 1px 2px #000, 0 0 4px #000;
    opacity: 0;
    transition: opacity 0.3s linear;
    word-wrap: break-word;
}
.toast--show    { opacity: 1; }
.toast--success { border-left-color: #51c551; }
.toast--error   { border-left-color: #fbb96a; }
.toast--info    { border-left-color: #38d5ea; }
.debug-overlay {
    position: fixed;
    top: 8px; left: 8px;
    z-index: ${Z_INDEX.toast};
    pointer-events: none;
    background: rgba(0,0,0,0.75);
    color: #ddd;
    font: 11px/1.25 Consolas, monospace;
    padding: 6px 8px;
    max-width: 520px;
    max-height: calc(100vh - 16px);
    overflow: hidden;
    border: 1px solid #444;
}
.debug-overlay .state { color: #9cf; margin-bottom: 4px; }
.debug-overlay .state b { color: #fff; font-weight: normal; margin-right: 4px; }
.debug-overlay .log   { color: #ccc; }
.debug-overlay .log .row { white-space: pre-wrap; }
.debug-overlay .log .t { color: #888; margin-right: 4px; }
.debug-overlay .log .warn  { color: #fbb96a; }
.debug-overlay .log .error { color: #ff8888; }
`.trim();

    function ensureStyles() {
        if (document.getElementById(STYLE_TAG_ID)) return;
        const style = document.createElement('style');
        style.id = STYLE_TAG_ID;
        style.textContent = STYLE_CSS;
        document.head.appendChild(style);
    }
    // #endregion

    // #region Input Blocking
    const INPUT_EVENTS = [
        "keydown", "keyup", "keypress",
        "mousedown", "mouseup", "click", "dblclick",
        "wheel", "contextmenu",
        "touchstart", "touchmove", "touchend",
        "pointerdown", "pointerup", "pointermove",
    ];

    let _blockerRefs = 0;
    let _blockerNode = null;
    let _blockerHandler = null;

    // Blocks and eats all input events (keyboard, mouse, touch, pointer) when active, except for:
    // - events originating from inside the allowInside element (to allow typing in modal forms)
    // - F5 keydown (no other way to return to the main menu)
    function pushInputBlock(allowInside) {
        _blockerRefs += 1;
        if (_blockerRefs > 1) return;

        _blockerNode = document.createElement('div');
        _blockerNode.className = 'blocker';
        document.body.appendChild(_blockerNode);

        _blockerHandler = (e) => {
            // Always allow F5 (return to title), F10 (debug overlay toggle).
            if (e.type === "keydown" && (e.key === "F5" || e.key === "F10")) return;

            if (allowInside && allowInside.contains(e.target)) return;

            // Outside the form: swallow the event entirely.
            e.stopImmediatePropagation();
            e.stopPropagation();
            e.preventDefault();
        };
        for (const ev of INPUT_EVENTS) {
            window.addEventListener(ev, _blockerHandler, true);
        }
    }

    function popInputBlock() {
        if (_blockerRefs === 0) return;
        _blockerRefs -= 1;
        if (_blockerRefs > 0) return;

        for (const ev of INPUT_EVENTS) {
            window.removeEventListener(ev, _blockerHandler, true);
        }
        _blockerHandler = null;
        if (_blockerNode && _blockerNode.parentNode) {
            _blockerNode.parentNode.removeChild(_blockerNode);
        }
        _blockerNode = null;
    }

    // We create wrappers around the input handlers so that we can
    // disable them when the blocker is active. Otherwise while we
    // have a modal form open the game would still react to keypresses
    // and mouse clicks.
    function wrap(obj, methodName) {
        if (!obj || typeof obj[methodName] !== 'function') return;
        const original = obj[methodName];
        obj[methodName] = function () {
            if (_blockerRefs > 0) return;
            return original.apply(this, arguments);
        };
    }

    function wrapInputs() {
        if (typeof Input !== 'undefined') {
            wrap(Input, '_onKeyDown');
            wrap(Input, '_onKeyUp');
            wrap(Input, '_onLostFocus');
        }
        if (typeof TouchInput !== 'undefined') {
            wrap(TouchInput, '_onMouseDown');
            wrap(TouchInput, '_onMouseMove');
            wrap(TouchInput, '_onMouseUp');
            wrap(TouchInput, '_onWheel');
            wrap(TouchInput, '_onTouchStart');
            wrap(TouchInput, '_onTouchMove');
            wrap(TouchInput, '_onTouchEnd');
            wrap(TouchInput, '_onTouchCancel');
            wrap(TouchInput, '_onPointerDown');
        }
    }

    wrapInputs();
    // #endregion


    // #region Utils
    const _DEBUG_LOG_MAX = 80;
    const _debugLog = [];
    function _formatArg(arg) {
        if (typeof arg === 'string') return arg;
        if (arg instanceof Error) return arg.stack || arg.message;
        try { return JSON.stringify(arg); } catch (e) { return String(arg); }
    }
    function _pushDebugLog(level, args) {
        const date = new Date();
        const time = ('0'+date.getHours()).slice(-2) + ':' +
                     ('0'+date.getMinutes()).slice(-2) + ':' +
                     ('0'+date.getSeconds()).slice(-2);
        const text = Array.prototype.map.call(args, _formatArg).join(' ');
        _debugLog.push({ time, level, text });
        if (_debugLog.length > _DEBUG_LOG_MAX) _debugLog.shift();
    }
    const log   = function(...args) { console.log("[YarimonoAP]", ...args);   _pushDebugLog('log',   args); };
    const warn  = function(...args) { console.warn("[YarimonoAP]", ...args);  _pushDebugLog('warn',  args); };
    const error = function(...args) { console.error("[YarimonoAP]", ...args); _pushDebugLog('error', args); };

    // We defer state-mutating actions when the game isn't ready for them:
    //  - In battle: the game snapshots save contents on battle start and
    //    restores them on end (Scene_InstantLoad in JsScript63Set.js). Any
    //    mutation during the battle is reverted, so we must wait.
    //  - Pre-init: on a fresh new game, $gameSystem.mZukan is empty until
    //    FirstPlayerSetting runs (called via CE 1 from CE 14). Touching mZukan
    //    before that breaks things, so we defer until after FirstPlayerSetting runs.
    function _isInBattle() {
        try { return typeof tempSave !== 'undefined' && tempSave != null; }
        catch (_) { return false; }
    }
    let _preInit = false
    function _isPreInit() {
        try { return _preInit; }
        catch (_) { return true; }
    }
    function _shouldDefer() {
        return _isInBattle() || _isPreInit();
    }

    const _deferQueue = [];
    /**
     * If we shouldn't apply game-state mutations right now, queue the function;
     * otherwise call it immediately. Drains via Scene_InstantLoad.start (post-
     * battle) or FirstPlayerSetting (post-init).
     */
    function deferOrCall(fn) {
        if (_shouldDefer()) {
            _deferQueue.push(fn);
            log(`deferring action; queue length now ${_deferQueue.length} (inBattle=${_isInBattle()} preInit=${_isPreInit()})`);
        } else {
            fn();
        }
    }
    function _drainDeferQueue() {
        if (_deferQueue.length === 0) return;
        log(`draining deferred queue (${_deferQueue.length} action(s))`);
        const q = _deferQueue.slice();
        _deferQueue.length = 0;
        // Put back into defer queue if needed, otherwise call.
        for (const fn of q) {
            try { deferOrCall(fn); }
            catch (e) { error(`deferred action threw: ${e && e.stack || e}`); }
        }
    }

    const _Scene_InstantLoad_start = Scene_InstantLoad.prototype.start;
    Scene_InstantLoad.prototype.start = function () {
        log("Scene_InstantLoad.start: draining defer queue after battle");
        _Scene_InstantLoad_start.apply(this, arguments);
        _drainDeferQueue();
    };
    const _FirstPlayerSetting = FirstPlayerSetting;
    FirstPlayerSetting = function () {
        log("FirstPlayerSetting: draining defer queue after init");
        _FirstPlayerSetting.apply(this, arguments);
        _preInit = false; // FirstPlayerSetting has run, so we're no longer in pre-init.
        _drainDeferQueue();
    };

    function uuid4() {
        const bytes = new Uint8Array(16);
        (window.crypto || window.msCrypto).getRandomValues(bytes);
        bytes[6] = (bytes[6] & 0x0f) | 0x40;
        bytes[8] = (bytes[8] & 0x3f) | 0x80;
        const hex = [...bytes].map(b => b.toString(16).padStart(2, '0'));
        return `${hex.slice(0, 4).join('')}-${hex.slice(4, 6).join('')}-` +
               `${hex.slice(6, 8).join('')}-${hex.slice(8, 10).join('')}-` +
               `${hex.slice(10, 16).join('')}`;
    }

    function normalizeHost(input) {
        // Prefer wss
        let scheme = "wss";
        let str = (input || "").trim();
        const match = str.match(/^(wss?):\/\/(.+)$/i);
        if (match) { scheme = match[1].toLowerCase(); str = match[2]; }
        if (!/:\d+$/.test(str)) str = `${str}:${DEFAULT_PORT}`;
        return { scheme, hostPort: str, url: `${scheme}://${str}` };
    }

    function yarimanIdFromGalleryIndex(idx) {
        const data = $N_Yariman_DB[idx];
        return data ? data.id : null;
    }
    
    let _yarimanIdToIndex = null;
    function galleryIndexFromYarimanId(id) {
        if (!_yarimanIdToIndex) {
            _yarimanIdToIndex = new Map();
            for (let i = 0; i < $N_Yariman_DB.length; i++) {
                _yarimanIdToIndex.set($N_Yariman_DB[i].id, i);
            }
        }
        const v = _yarimanIdToIndex.get(id);
        return v != null ? v : -1;
    }

    
    function makeRng(seed) {
        let s = (seed | 0) >>> 0;
        return function () {
            s = (s + 0x6D2B79F5) >>> 0;
            let t = s;
            t = Math.imul(t ^ (t >>> 15), t | 1);
            t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
            return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        };
    }

    function resolveItemName(locId) {
        const networkItem = scoutedItems[locId];
        return networkItem
            ? client.itemName(networkItem.player, networkItem.item)
            : `AP Item at ${locId}`;
    }
    // #endregion

    // #region Debug Overlay
    let _debugOverlayNode = null;
    let _debugOverlayTick = null;

    function _escapeHtml(str) {
        return String(str).replace(/[&<>"']/g, c => ({
            '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'
        }[c]));
    }

    function _gatherDebugState() {
        const res = {};
        try { res.mapId      = $gameMap && $gameMap.mapId(); } catch (e) {}
        try { res.mapName    = $dataMapInfos && res.mapId != null && $dataMapInfos[res.mapId] && $dataMapInfos[res.mapId].name; } catch (e) {}
        try { res.player     = $gamePlayer && `(${$gamePlayer.x}, ${$gamePlayer.y})`; } catch (e) {}
        try { res.trainerLv  = $gameSystem && $gameSystem.TrainerLv; } catch (e) {}
        try { res.eventRun   = $gameMap && $gameMap.isEventRunning(); } catch (e) {}
        try { res.eventId    = $gameMap && $gameMap._interpreter && $gameMap._interpreter._eventId; } catch (e) {}
        try { res.inBattle   = _isInBattle(); } catch (e) {}
        res.client    = client ? 'connected' : 'none';
        if (client) {
            try { res.slot       = client.slotInfo && (client.slotInfo.slot + ' (' + client.slot + ')'); } catch (e) {}
            try { res.checked    = ($gameSystem && $gameSystem.AP && $gameSystem.AP.checkedLocations && $gameSystem.AP.checkedLocations.length) || 0; } catch (e) {}
            try { res.lastRecv   = SaveStorage.get($gameSystem, 'lastReceivedIndex'); } catch (e) {}
        }
        return res;
    }

    function _redrawDebugOverlay() {
        if (!_debugOverlayNode) return;
        const state = _gatherDebugState();
        const stateRows = Object.keys(state).map(key =>
            `<div><b>${_escapeHtml(key)}</b>${_escapeHtml(state[key] === null ? '—' : state[key])}</div>`
        ).join('');
        const tail = _debugLog.slice(-30);
        const logRows = tail.map(log =>
            `<div class="row ${log.level}"><span class="t">${log.time}</span>${_escapeHtml(log.text).slice(0, 240)}</div>`
        ).join('');
        _debugOverlayNode.innerHTML =
            `<div class="state">${stateRows}</div><div class="log">${logRows}</div>`;
    }

    function _toggleDebugOverlay() {
        if (_debugOverlayNode) {
            if (_debugOverlayNode.parentNode) _debugOverlayNode.parentNode.removeChild(_debugOverlayNode);
            _debugOverlayNode = null;
            if (_debugOverlayTick != null) { clearInterval(_debugOverlayTick); _debugOverlayTick = null; }
            return;
        }
        ensureStyles();
        _debugOverlayNode = document.createElement('div');
        _debugOverlayNode.className = 'debug-overlay';
        document.body.appendChild(_debugOverlayNode);
        _redrawDebugOverlay();
        _debugOverlayTick = setInterval(_redrawDebugOverlay, 250);
    }

    window.addEventListener('keydown', (e) => {
        if (e.key === 'F10') {
            e.preventDefault();
            e.stopPropagation();
            _toggleDebugOverlay();
        }
    }, true);
    // #endregion

    // #region Event Bus
    class EventBus {
        constructor() { this._handlers = new Map(); }
        on(event, fn) {
            if (!this._handlers.has(event)) this._handlers.set(event, []);
            this._handlers.get(event).push(fn);
            return () => this.off(event, fn);
        }
        off(event, fn) {
            const arr = this._handlers.get(event);
            if (!arr) return;
            const i = arr.indexOf(fn);
            if (i >= 0) arr.splice(i, 1);
        }
        emit(event, data) {
            const arr = this._handlers.get(event);
            if (!arr) return;
            for (const fn of [...arr]) {
                try { fn(data); }
                catch (e) { error(`handler for "${event}" threw:`, e); }
            }
        }
    }
    // #endregion


    // #region Archipelago Client
    class APClient {
        /**
         * @param {object} opts
         * @param {string} opts.host
         * @param {string} opts.slot
         * @param {string} [opts.password]
         * @param {string} [opts.uuid]
         * @param {boolean} [opts.offline]
         */
        constructor(opts) {
            this.host = opts.host;
            this.slot = opts.slot;
            this.password = opts.password || "";
            this.uuid = opts.uuid || uuid4();
            this.offline = opts.offline || false;

            this.socket = null;
            this.connected = false;
            this.slotInfo = null;
            this.roomInfo = null;
            this.slot_data = null;

            if (this.offline) {
                this.slot_data = SaveStorage.get($gameSystem, 'offlineSlotData') || null;
                scoutedItems = SaveStorage.get($gameSystem, 'offlineScoutedItems') || {};
            }

            this.dataPackage = Storage.get('dataPackage') || {};
            this._reconnectAttempt = 0;
            this._intentionalClose = false;
            this._dataPackageReady = false;
            this._heldToasts = [];
            this._hasConnectedOnce = false;

            this.events = new EventBus();
        }

        
        _toastItem(item) {
            let itemName = this.ownItemName(item.item);
            let locationName = this.locationName(item.player, item.location);
            let playerName = this.playerName(item.player);
            showToast(`Received item "${itemName || item.item}" from ${playerName || item.player} (${locationName || item.location})`, { variant: 'success', ms: 10000 });
        }

        _maybeRequestDataPackage(roomInfo) {
            const checksums = (roomInfo && roomInfo.datapackage_checksums) || {};
            const stale = [];
            for (const game of Object.keys(checksums)) {
                const cached = this.dataPackage[game];
                if (!cached || cached.checksum !== checksums[game]) {
                    stale.push(game);
                }
            }
            if (stale.length === 0) {
                log("dataPackage cache hot for", Object.keys(checksums).join(", "));
                this._dataPackageReady = true;
                this.events.emit("dataPackageReady", this.dataPackage);
                return;
            }
            log(`requesting DataPackage for ${stale.join(", ")}`);
            this._send({ cmd: "GetDataPackage", games: stale });
        }

        _ingestDataPackage(msg) {
            const games = (msg.data && msg.data.games) || {};
            for (const game of Object.keys(games)) {
                this.dataPackage[game] = games[game];
                delete this.dataPackage[game]._itemById;
                delete this.dataPackage[game]._locationById;
            }
            Storage.set('dataPackage', this.dataPackage);
            log("dataPackage updated for", Object.keys(games).join(", "));
            this.events.emit("dataPackageReady", this.dataPackage);
        }

        _scoutAllPlaceholders() {
            const ids = [];
            // Shop slots
            const num = (this.slot_data && this.slot_data.extra_levels) | 0;
            for (let i = 0; i < num; i++) ids.push(LOCATION_IDS.EXTRA_SHOP + i);
            // Chests / pickups (19 per game, starting at LOCATION_IDS.PICKUP)
            for (let i = LOCATION_IDS.PICKUP; i < LOCATION_IDS.PICKUP + 19; i++) {
                ids.push(i);
            }
            // Mens bath
            ids.push(MENS_BATH_LEVEL_LOC_ID);
            // Jizo final reward
            ids.push(JIZO_SET_COMPLETE_LOC_ID);
            // VIP card pickup
            ids.push(VIP_CARD_LOC_ID);
            // All the event shop items
            for (let i = 0; i < EVENT_SHOP_ITEM_IDS.length; i++) {
                ids.push(LOCATION_IDS.EVENT_PURCHASE + EVENT_SHOP_ITEM_IDS[i]);
            }
            // All mushrooms
            for (const locId of MUSHROOM_LOCATIONS) ids.push(locId);
            // Leo Big City fight
            ids.push(LEO_BIG_CITY_LOC_ID);
            if (ids.length) this.sendLocationScouts(ids);
        }

        /**
         * Compare our local checked-set to the server's `checked_locations`
         * from the Connected data and resend anything we have that the
         * server doesn't.
         */
        _reconcileChecks(connectedMsg) {
            const local = ($gameSystem && $gameSystem.AP && $gameSystem.AP.checkedLocations) || [];
            if (local.length === 0) return;
            const serverChecked = new Set(connectedMsg.checked_locations || []);
            const missing = local.filter(id => !serverChecked.has(id));
            if (missing.length === 0) return;
            log(`reconciling ${missing.length} offline check(s) with server`);
            this._send({ cmd: "LocationChecks", locations: missing });
        }

        /** Return the game name for a given slot id, or null. */
        playerGame(slotId) {
            // Slot 0 is special Archipelago slot.
            if (slotId === 0) return "Archipelago";
            const si = this.slotInfo && this.slotInfo.slot_info;
            const e = si && si[slotId];
            return (e && e.game) || null;
        }

        /** Return the slot's display name (alias if set, else name). */
        playerName(slotId) {
            const si = this.slotInfo && this.slotInfo.slot_info;
            const e = si && si[slotId];
            return (e && (e.alias || e.name)) || `slot${slotId}`;
        }

        /** Resolve (slotId, itemId) → item display name via that slot's DataPackage. */
        itemName(slotId, itemId) {
            const pkg = this._pkgForSlot(slotId);
            const m = pkg && this._reverse(pkg, 'item_name_to_id', '_itemById');
            return (m && m.get(itemId)) || `item#${itemId}`;
        }

        /** Resolve (slotId, locationId) → location display name via that slot's DataPackage. */
        locationName(slotId, locationId) {
            // Location -1 is Cheat, -2 is Server.
            if (locationId === -1) return "Cheat";
            if (locationId === -2) return "Server";
            const pkg = this._pkgForSlot(slotId);
            const m = pkg && this._reverse(pkg, 'location_name_to_id', '_locationById');
            return (m && m.get(locationId)) || `loc#${locationId}`;
        }

        /** Resolve an item id in our slot's game. */
        ownItemName(itemId) {
            return this.itemName(this.slotInfo && this.slotInfo.slot, itemId);
        }

        /** Resolve a location id in our slot's game. */
        ownLocationName(locationId) {
            return this.locationName(this.slotInfo && this.slotInfo.slot, locationId);
        }

        _pkgForSlot(slotId) {
            const game = this.playerGame(slotId);
            return game ? this.dataPackage[game] : null;
        }

        _reverse(pkg, forwardField, cacheField) {
            if (pkg[cacheField]) return pkg[cacheField];
            const map = new Map();
            const src = pkg[forwardField] || {};
            for (const name of Object.keys(src)) map.set(src[name], name);
            pkg[cacheField] = map;
            return map;
        }


        on(event, fn) { return this.events.on(event, fn); }

        /** Open the socket and complete the AP auth handshake. */
        async connect() {
            this._intentionalClose = false;
            await this._openSocket();
            await this._authenticate();
        }

        /** Close the socket and stop reconnect attempts. */
        close() {
            this._intentionalClose = true;
            if (this.socket) {
                try { this.socket.close(); } catch (e) {}
            }
        }

        /** 
         * Tell the server which AP locations have been checked.
         * Wire packet fires immediately; local cache marking is deferred if
         * we're mid-battle so it survives the InstantLoad snapshot revert.
         */
        sendLocationChecks(locationIds) {
            const fresh = locationIds.filter(id => !SaveStorage.isLocationChecked($gameSystem, id));
            if (fresh.length === 0) return;
            this._send({ cmd: "LocationChecks", locations: fresh });
            deferOrCall(() => {
                for (const id of fresh) SaveStorage.markLocationChecked($gameSystem, id);
            });
        }

        /** 
         * Ask the server what items live at the given locations.
         */
        sendLocationScouts(locationIds, createAsHint = 0) {
            if (!locationIds || locationIds.length === 0) return;
            this._send({ cmd: "LocationScouts", locations: locationIds, create_as_hint: createAsHint });
        }

        /** Mark this slot as having completed its goal. */
        sendGoalComplete() {
            this._send({ cmd: "StatusUpdate", status: CLIENT_GOAL });
        }

        /** Send a chat message to the room. */
        say(text) {
            this._send({ cmd: "Say", text: String(text) });
        }

        _openSocket() {
            return new Promise((resolve, reject) => {
                let { scheme, hostPort, url } = normalizeHost(this.host);
                log(`opening ${url}`);

                let socket;
                let retriedWithAlternateScheme = false;
                function connect(forcedScheme) {
                    if (forcedScheme) {
                        url = `${forcedScheme}://${hostPort}`;
                        log(`attempting connection with ${forcedScheme}:// scheme to ${hostPort}`);
                    }
                    try { socket = new WebSocket(url); }
                    catch (e) {
                        return reject(new Error(`WebSocket threw: ${e.message || e}`));
                    }
                    this.socket = socket;

                    const timeout = setTimeout(() => {
                        try { socket.close(); } catch (e) {}
                        reject(new Error(`Connect timed out after ${CONNECT_TIMEOUT_MS}ms to ${url}`));
                    }, CONNECT_TIMEOUT_MS);

                    socket.onopen = () => {
                        clearTimeout(timeout);
                        log("socket open");
                        resolve();
                    };
                    socket.onclose = (ev) => {
                        clearTimeout(timeout);
                        const detail = `code=${ev.code} reason=${ev.reason || '<none>'} wasClean=${ev.wasClean}`;
                        if (!this.connected) {
                            // Failed before/during auth.
                            if (!retriedWithAlternateScheme) {
                                // Try again with whatever scheme we didn't try before.
                                if (scheme === "wss") {
                                    log(`retrying with ws:// instead of wss:// for ${hostPort}`);
                                    retriedWithAlternateScheme = true;
                                    connect.call(this, "ws");
                                    return;
                                } else if (scheme === "ws") {
                                    log(`retrying with wss:// instead of ws:// for ${hostPort}`);
                                    retriedWithAlternateScheme = true;
                                    connect.call(this, "wss");
                                    return;
                                }
                            }
                            reject(new Error(`WebSocket closed before connect: ${detail} (url=${url})`));
                        } else {
                            warn(`socket closed: ${detail}`);
                            this.connected = false;
                            this.events.emit("disconnected", { code: ev.code, reason: ev.reason });
                            this._scheduleReconnect();
                        }
                    };
                    socket.onerror = () => {};
                    socket.onmessage = (ev) => this._onMessage(ev.data);
                }
                connect.call(this);
            });
        }

        _authenticate() {
            return new Promise((resolve, reject) => {
                let settled = false;
                const offConnected = this.events.on("_authConnected", (data) => {
                    if (settled) return;
                    settled = true;
                    clearTimeout(timer);
                    offConnected(); offRefused();
                    this.connected = true;
                    this.slotInfo  = data;
                    this._reconnectAttempt = 0;
                    log("authenticated as", data.slot, "in team", data.team);
                    resolve(data);
                });
                const offRefused = this.events.on("_authRefused", (data) => {
                    if (settled) return;
                    settled = true;
                    clearTimeout(timer);
                    offConnected(); offRefused();
                    const reasons = (data.errors || []).join(", ") || "<no reason>";
                    reject(new Error(`Server refused connection: ${reasons}`));
                });
                const timer = setTimeout(() => {
                    if (settled) return;
                    settled = true;
                    offConnected(); offRefused();
                    reject(new Error(`No Connected/ConnectionRefused within ${AUTH_TIMEOUT_MS}ms`));
                }, AUTH_TIMEOUT_MS);

                this._send({
                    cmd: "Connect",
                    game: GAME,
                    name: this.slot,
                    password: this.password,
                    version: AP_VERSION,
                    tags: [],
                    items_handling: ITEMS_HANDLING_ALL,
                    uuid: this.uuid,
                    slot_data: true,
                });
            });
        }

        _send(obj) {
            if (this.offline) {
                log("offline mode, not sending:", obj);
                return;
            }
            if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
                warn("dropping send, socket not open:", obj.cmd);
                return;
            }
            try { this.socket.send(JSON.stringify([obj])); }
            catch (e) { error("send failed:", e, obj); }
        }

        _onMessage(raw) {
            let msgs;
            try { msgs = JSON.parse(raw); }
            catch (e) { return error("bad JSON from server:", raw); }
            if (!Array.isArray(msgs)) {
                return error("server data was not an array:", msgs);
            }
            for (const msg of msgs) this._dispatch(msg);
        }

        _dispatch(msg) {
            const cmd = msg && msg.cmd;
            switch (cmd) {
                case "RoomInfo":
                    this.roomInfo = msg;
                    this.events.emit("roomInfo", msg);
                    this._maybeRequestDataPackage(msg);
                    break;
                case "Connected":
                    this.events.emit("_authConnected", msg);
                    this.events.emit("connected", msg);
                    this.slot_data = msg.slot_data || null;
                    SaveStorage.set($gameSystem, 'offlineSlotData', this.slot_data);
                    this._hasConnectedOnce = true;
                    this._scoutAllPlaceholders();
                    this._reconcileChecks(msg);
                    break;
                case "ConnectionRefused":
                    this.events.emit("_authRefused", msg);
                    break;
                case "ReceivedItems": {
                    log(`ReceivedItems: index=${msg.index} count=${msg.items.length}`);
                    // We may receive items while in battle, but were we to apply them then, the InstantLoad at battle
                    // end would revert those changes. Instead we defer those changes until after the battle.
                    deferOrCall(() => {
                        let lastReceived = SaveStorage.get($gameSystem, 'lastReceivedIndex');
                        lastReceived = typeof lastReceived === 'number' ? lastReceived : -1;
                        const start = msg.index;
                        log(`Acting on ReceivedItems index=${start} count=${msg.items.length} lastReceived=${lastReceived} skipping=${Math.max(0, lastReceived - start + 1)}`);
                        msg.items.forEach((it, i) => {
                            const idx = start + i;
                            if (idx <= lastReceived) return;
                            lastReceived = idx;
                            SaveStorage.set($gameSystem, 'lastReceivedIndex', idx);
                            log(`Emitting itemReceived for index=${idx}`);
                            this.events.emit("itemReceived", { index: idx, item: it });
                            if (this._dataPackageReady) {
                                this._toastItem(it);
                            } else {
                                this._heldToasts.push(it);
                            }
                        });
                    });
                    break;
                }
                case "LocationInfo": this.events.emit("locationInfo", msg); break;
                case "RoomUpdate": this.events.emit("roomUpdate", msg); break;
                case "PrintJSON": this.events.emit("print", msg); break;
                case "DataPackage":
                    this._ingestDataPackage(msg);
                    this._dataPackageReady = true;
                    this._heldToasts.forEach((it) => this._toastItem(it));
                    this._heldToasts = [];
                    this.events.emit("dataPackage", msg);
                    break;
                case "Bounced": this.events.emit("bounced", msg); break;
                case "InvalidPacket":
                    warn("server says we sent an invalid packet:", msg);
                    break;
                default:
                    log("unhandled cmd:", cmd, msg);
            }
        }

        _scheduleReconnect() {
            if (this._intentionalClose) return;
            const delay = RECONNECT_DELAYS_MS[
                Math.min(this._reconnectAttempt, RECONNECT_DELAYS_MS.length - 1)
            ];
            this._reconnectAttempt += 1;
            log(`reconnecting in ${delay}ms (attempt ${this._reconnectAttempt})`);
            setTimeout(() => {
                this.connect().catch((e) => {
                    warn("reconnect failed:", e.message);
                    this._scheduleReconnect();
                });
            }, delay);
        }
    }
    // #endregion

    // #region Storage
    /**
     * Local storage wrapper.
     */
    const Storage = {
        _key(key) { return `yarimono_ap_${key}`; },
        /** Get a value from storage by key. Returns null if not found or if parsing fails. */
        get(key) {
            const v = localStorage.getItem(this._key(key));
            if (v === null) return null;
            try { return JSON.parse(v); } catch (e) { return null; }
        },
        /** Set a value in storage by key. */
        set(key, value) {
            localStorage.setItem(this._key(key), JSON.stringify(value));
        },
        /** Remove a value from storage by key. */
        remove(key) {
            localStorage.removeItem(this._key(key));
        },
    };
    // #endregion

    // #region Save Storage
    let cachedCheckSet = null; // cache to avoid finding checked locations in an array every time
    /**
     * AP-related state stored in the save file under $gameSystem.AP.
     */
    const SaveStorage = {
        /** Check if this save file has AP data. */
        isAPSave(gameSystem) {
            return gameSystem && gameSystem.AP && gameSystem.AP.isAPSave;
        },
        /** Mark this save file as having AP data, initializing the AP object if needed. */
        markAPSave(gameSystem) {
            if (!gameSystem) throw new Error("No game system");
            if (!gameSystem.AP) gameSystem.AP = {};
            gameSystem.AP.isAPSave = true;
        },
        /** Get a value from the AP save data by key. Returns null if not an AP save or if key not found. */
        get(gameSystem, key) {
            if (!this.isAPSave(gameSystem)) return null;
            return gameSystem.AP[key];
        },
        /** Set a value in the AP save data by key. */
        set(gameSystem, key, value) {
            if (!this.isAPSave(gameSystem)) return;
            gameSystem.AP[key] = value;
        },
        /** Mark a location as checked in the AP save data. */
        markLocationChecked(gameSystem, locationId) {
            if (!this.isAPSave(gameSystem)) return;
            if (!gameSystem.AP.checkedLocations) {
                gameSystem.AP.checkedLocations = [];
            }
            if (!cachedCheckSet) {
                cachedCheckSet = new Set(gameSystem.AP.checkedLocations);
            }
            if (!cachedCheckSet.has(locationId)) {
                cachedCheckSet.add(locationId);
                gameSystem.AP.checkedLocations.push(locationId);
            }
        },
        /** Check if a location is marked as checked in the AP save data. */
        isLocationChecked(gameSystem, locationId) {
            if (!this.isAPSave(gameSystem)) return false;
            if (!cachedCheckSet) {
                cachedCheckSet = new Set(gameSystem.AP.checkedLocations || []);
            }
            return cachedCheckSet.has(locationId);
        },
        /** Remove a value from the AP save data by key. */
        remove(gameSystem, key) {
            if (!this.isAPSave(gameSystem)) return;
            delete gameSystem.AP[key];
        },
    }
    // #endregion

    // #region UI
    /**
     * Modal prompt that blocks game input while it's open.
     * @param {string} title - The title to show at the top of the modal.
     * @param {Array<{name: string, type: string, value?: string}>} inputs - List of input fields to show. Type is any valid HTML input type.
     * @param {object} [options] - Optional settings.
     * @param {Array<{label: string, primary?: boolean, cancel?: boolean}>} [options.buttons] - List of buttons to show. Primary button triggers on Enter, cancel button triggers on Esc.
     * @returns {Promise<{label: string, values: Array<string>|null}>} Resolves when the user clicks a button. Values is an array of input values in the same order as the inputs argument, or null if the cancel button was used.
     */
    function promptInput(title, inputs, options) {
        ensureStyles();
        options = options || {};
        const buttons = options.buttons || [
            { label: 'OK', primary: true },
            { label: 'Cancel', cancel: true },
        ];

        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.className = 'modal';

            const card = document.createElement('form');
            card.className = 'card';

            const heading = document.createElement('h2');
            heading.textContent = title;
            card.appendChild(heading);

            const inputElems = inputs.map(input => {
                const field = document.createElement('div');
                field.className = 'field';
                const label = document.createElement('label');
                label.textContent = input.name;
                const inputElem = document.createElement('input');
                inputElem.type = input.type;
                if (input.value != null) inputElem.value = input.value;
                inputElem.autocomplete = 'off';
                inputElem.spellcheck = false;
                field.appendChild(label);
                field.appendChild(inputElem);
                card.appendChild(field);
                return inputElem;
            });

            const cleanup = () => {
                popInputBlock();
                if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
                document.removeEventListener('keydown', onKeyDown, true);
            };
            const finish = (button) => {
                const values = button.cancel ? null : inputElems.map(el => el.value);
                cleanup();
                resolve({ label: button.label, values });
            };

            const primary = buttons.find(b => b.primary) || buttons[0];
            const cancel  = buttons.find(b => b.cancel);

            const actions = document.createElement('div');
            actions.className = 'actions';
            buttons.forEach(b => {
                const btn = document.createElement('button');
                btn.type = b.primary ? 'submit' : 'button';
                btn.className = 'btn';
                btn.textContent = b.label;
                btn.style.marginRight = '6px';
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    finish(b);
                });
                actions.appendChild(btn);
            });
            card.appendChild(actions);

            card.addEventListener('submit', (e) => {
                e.preventDefault();
                finish(primary);
            });

            // If cancel button exists, allow Esc key to trigger it.
            const onKeyDown = (e) => {
                if (e.key === 'Escape' && cancel) {
                    e.preventDefault();
                    e.stopPropagation();
                    finish(cancel);
                }
            };
            document.addEventListener('keydown', onKeyDown, true);

            overlay.appendChild(card);
            document.body.appendChild(overlay);
            pushInputBlock(card);

            // Focus first empty field.
            const firstEmpty = inputElems.find(el => !el.value);
            (firstEmpty || inputElems[0]).focus();
        });
    }

    /**
     * Non-blocking toast notification that disappears after a few seconds. Appears in the top right corner.
     * @param {string} message - The message to show in the toast.
     * @param {object} [options] - Optional settings.
     * @param {'success'|'error'|'info'} [options.variant] - The visual style of the toast.
     * @param {number} [options.ms] - How long to show the toast before fading out, in milliseconds.
     */
    function showToast(message, options) {
        ensureStyles();
        options = options || {};
        const variant = options.variant || 'info';
        const ms = options.ms || 5000;

        let host = document.getElementById('toast-container');
        if (!host) {
            host = document.createElement('div');
            host.id = 'toast-container';
            host.className = 'toast-container';
            document.body.appendChild(host);
        }

        const toast = document.createElement('div');
        toast.className = `toast toast--${variant}`;
        toast.textContent = message;
        host.appendChild(toast);

        requestAnimationFrame(() => requestAnimationFrame(() => {
            toast.classList.add('toast--show');
        }));

        setTimeout(() => {
            toast.classList.remove('toast--show');
            setTimeout(() => {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 250);
        }, ms);
    }
    // #endregion

    // #region Function Overrides

    // Game_Interpreter.prototype.Btl_End_ExpUpdate controls the end of battle exp reward
    // for Yarimon. It's also the best place to set the flag BトレーナーLv上げないFlg to
    // prevent fights from giving trainer levels and grant AP checks for beating trainers
    // for the first time.
    const _Btl_End_ExpUpdate = Game_Interpreter.prototype.Btl_End_ExpUpdate;
    Game_Interpreter.prototype.Btl_End_ExpUpdate = function() {
        if (!client) return _Btl_End_ExpUpdate.apply(this, arguments);
        // If it's a wild Yarimon battle, do nothing.
        if (battle_Class.isYasei) return _Btl_End_ExpUpdate.apply(this, arguments);

        // The flag BトレーナーLv上げないFlg controls whether a level would occur.
        // We never want to allow the game to give a level through battle.
        BトレーナーLv上げないFlg = true;

        // Now we check if we've beated the trainer before to see if we
        // should mark this trainer's level up as checked.
        let hasWon = $gameSystem.WinedTrainerArr.indexOf(btlTrainerId) === -1;
        if (hasWon) {
            $gameSystem.WinedTrainerArr.push(btlTrainerId);
            log(`Defeated trainer ${btlTrainerId} for the first time. Marking level up as checked.`);
            let locationId = LOCATION_IDS.TRAINER_FIGHT + btlTrainerId;
            if (client.ownLocationName(locationId) === null) {
                // A trainer fight that isn't in the AP location list.
                // Just accept the level up without sending a check, but
                // log a warning since that isn't supposed to happen.
                warn(`No AP location for trainer fight ${btlTrainerId} (locationId=${locationId})`);
            } else {
                client.sendLocationChecks([locationId]);
            }
        }

        // Send the goal if the trainer was the goal boss. This would only catch
        // Athena and Nupuryu. White God and Tama have other handling.
        if (client.slot_data.goal) {
            let goalTrainerId = GOAL_TRAINER_IDS[client.slot_data.goal];
            if (btlTrainerId === goalTrainerId) {
                log(`Defeated goal trainer ${btlTrainerId}, sending goal complete.`);
                client.sendGoalComplete();
            }
        }

        return _Btl_End_ExpUpdate.apply(this, arguments)
    }

    // The game would normally unlock the H-scenes in the Yariman Encyclopedia when
    // MenuHSceneOpen is called. Instead, we intercept it and mark the location as checked.
    const _MenuHSceneOpen = MenuHSceneOpen;
    MenuHSceneOpen = function(_charaId, No) {
        if (client && client.slot_data.randomize_yariman_encyclopedia) {
            let charNo = galleryIndexFromYarimanId(_charaId);
            let locId = _sceneLocationId(charNo, No);
            log(`H-scene unlocked for char ${charNo} scene ${No}, marking location ${locId} as checked.`);
            client.sendLocationChecks([locId]);
            return
        }
        if (client && client.slot_data.encyclopedia_ct_bonus > 0) {
            recalculateCheatTackleBonus();
        }
        return _MenuHSceneOpen.apply(this, arguments);
    };

    // To know when switch-based locations are checked.
    const _Switches_setValue = Game_Switches.prototype.setValue;
    Game_Switches.prototype.setValue = function (id, value, forceNormal) {
        if (client && !forceNormal) {
            // Range that correspond to the ultimate move unlocks for each element.
            if (id >= SWITCH_ULTIMATE_MOVE_START && id < SWITCH_ULTIMATE_MOVE_START + SWITCH_ULTIMATE_COUNT) {
                log(`Ultimate move unlocked for element with switch ${id}, marking location as checked.`);
                let locId = LOCATION_IDS.ULTIMATE_MOVE + id;
                client.sendLocationChecks([locId]);

                // Prevent the game from actually setting the switch on, since that would unlock the move.
                return;
            } else if (DREAM_SWITCH_SET.has(id)) {
                log(`Dream switch ${id} turned on, marking location as checked.`);
                let key = Object.keys(DREAM_SWITCHES).find(k => DREAM_SWITCHES[k] === id);
                let locId = DREAM_LOC_IDS[key];
                if (locId === undefined) {
                    warn(`No AP location for dream switch ${id}`);
                } else {
                    client.sendLocationChecks([locId]);
                }
            }
        }
        return _Switches_setValue.call(this, id, value);
    }

    // To know when shop items are gained.
    const _gameParty_gainItem = Game_Party.prototype.gainItem;
    Game_Party.prototype.gainItem = function (item, amount, includeEquip) {
        if (client) {
            // Watch for the shop ap items, mark them checked when gained, and
            // prevent them from actually being added to the inventory.
            let id = item.id - 1 // Game has item ids 1-based but AP location ids are 0-based
            if (id >= EVENT_SHOP_ITEM_ID_BASE && id < AP_SHOP_ITEM_ID_BASE) {
                let locId = LOCATION_IDS.EVENT_PURCHASE + (id - EVENT_SHOP_ITEM_ID_BASE);
                log(`Event shop item gained with id ${item.id}, marking location ${locId} as checked.`);
                client.sendLocationChecks([locId]);
                return;
            } else if (id >= AP_SHOP_ITEM_ID_BASE) {
                let locId = LOCATION_IDS.EXTRA_SHOP + (id - AP_SHOP_ITEM_ID_BASE);
                log(`AP shop item gained with id ${item.id}, marking location ${locId} as checked.`);
                client.sendLocationChecks([locId]);
                return;
            }
        }
        return _gameParty_gainItem.call(this, item, amount, includeEquip);
    }
    // #endregion


    // #region Yariman Encyclopedia Modifications
    function _sceneLocationId(charNo, sceneIndex) {
        // AP location ids for h-scenes are assigned as:
        //   base + charNo * 10 + sceneIndex
        // where base = LOCATION_IDS.SCENE_UNLOCK.
        return LOCATION_IDS.SCENE_UNLOCK + charNo * 10 + sceneIndex;
    }

    function _itemSceneIndex(itemId) {
        // Inverse of sceneLocationId: given an itemId, return { charNo, sceneIndex } if it's in the h-scene range, else null.
        if (itemId < ITEM_IDS.SCENE_UNLOCK) return null;
        const offset = itemId - ITEM_IDS.SCENE_UNLOCK;
        const charNo = Math.floor(offset / 10);
        const sceneIndex = offset % 10;
        return { charNo, sceneIndex };
    }

    /**
     * Unlocks the given scene for the given character in the Yariman Encyclopedia.
     * @param {number} charNo - The character number.
     * @param {number} sceneIndex - The scene index for that character.
     */
    function unlockScene(charNo, sceneIndex) {
        let db = $N_Yariman_DB[charNo];
        let entry = $gameSystem.mZukan[charNo];
        if (!db || !entry) {
            warn(`Trying to unlock scene ${charNo}/${sceneIndex} but no DB or entry found.`);
            return;
        }
        _MenuHSceneOpen(entry.id, sceneIndex);
        log(`unlocked scene ${charNo}/${sceneIndex} (${db.name})`);
        recalculateCheatTackleBonus();
    }

    // Backfills an mZukan entry so DetailDraw can iterate its arrays safely.
    function _ensureZukanEntry(No) {
        const db = $N_Yariman_DB[No];
        if (!db) return null;
        if (!$gameSystem.mZukan[No]) {
            $gameSystem.mZukan[No] = {
                id: db.id, lookFlg: false, getFlg: false,
                hSceneFlg: [], hTatieFlg: [],
            };
        }
        let entry = $gameSystem.mZukan[No];
        if (!entry.hSceneFlg) entry.hSceneFlg = [];
        if (!entry.hTatieFlg) entry.hTatieFlg = [];
        const sceneCount = (db.hScene && db.hScene.length) || 0;
        const tatieCount = (db.tatiePic && db.tatiePic.tatieDatas && db.tatiePic.tatieDatas.length) || 0;
        while (entry.hSceneFlg.length < sceneCount) entry.hSceneFlg.push(false);
        while (entry.hTatieFlg.length < tatieCount) entry.hTatieFlg.push(false);
        return entry;
    }
    

    // Show every name in the list.
    const _GetZukanName_No = GetZukanName_No;
    GetZukanName_No = function (No) {
        if (!client || !client.slot_data.randomize_yariman_encyclopedia) 
            return _GetZukanName_No(No);

        if (Zukan_YarimanFlg && $N_Yariman_DB[No]) {
            let name = $N_Yariman_DB[No].name || "";
            // Pad to 9 chars and diplay count of checked/total scenes if any.
            name = name.padEnd(9, " ");
            const db = $N_Yariman_DB[No];
            const checked = db.hScene.map((_, i) => SaveStorage.isLocationChecked($gameSystem, _sceneLocationId(No, i))).filter(Boolean).length;
            const total = db.hScene.length;
            if (total > 0) {
                name += ` (${checked}/${total})`;
            }
            return name;
        }
        return _GetZukanName_No(No);
    };

    // So DetailDraw doesn't explode when trying to open an entry where we haven't actually found any scenes.
    // Also modifies what's shown so we always get the hint text.
    const _GetZukanData_No = GetZukanData_No;
    GetZukanData_No = function (No) {
        if (!client || !client.slot_data.randomize_yariman_encyclopedia) 
            return _GetZukanData_No(No);

        if (Zukan_YarimanFlg) {
            const db = $N_Yariman_DB[No];
            if (!db) return _GetZukanData_No(No);
            const entry = $gameSystem.mZukan[No];
            const dbEntry = new ZukanData(db.zukanPicPath);
            // Makes it not explode
            dbEntry.hScene = db.hScene;
            // Makes the hint be shown on the profile.
            dbEntry.cProfile.hint = db.cProfile.hint;
            // If actually "found", give back the real row (full stats).
            if (entry && entry.getFlg) {
                const full = Object.assign({}, db, {
                    cProfile: Object.assign({}, db.cProfile, { hint: "look" }),
                    picPath: db.zukanPicPath,
                    _realHint: db.cProfile.hint,
                });
                return full;
            }
            return dbEntry;
        }
        return _GetZukanData_No(No);
    };

    // Modified to make sure it doesn't break with everything visible and also to show
    // checked scenes as checked and unchecked scenes with their hint.
    const _Menu_Zukan_DetailDraw = Game_Interpreter.prototype.Menu_Zukan_DetailDraw;
    Game_Interpreter.prototype.Menu_Zukan_DetailDraw = function (ckMode) {
        if (!client || !client.slot_data.randomize_yariman_encyclopedia) 
            return _Menu_Zukan_DetailDraw.call(this, ckMode);

        _ensureZukanEntry(ckMode.selNo - 1);
        _Menu_Zukan_DetailDraw.call(this, ckMode);
        if (!Zukan_YarimanFlg) return;

        const No = ckMode.selNo - 1;
        const entry  = $gameSystem.mZukan[No];
        const db = $N_Yariman_DB[No];
        if (!entry || !db) return;

        for (let i = 0; i < entry.hSceneFlg.length; i++) {
            const locId   = _sceneLocationId(No, i);
            const checked = SaveStorage.isLocationChecked($gameSystem, locId);
            const itemGotten = entry.hSceneFlg[i];
            const zureX = (i % 2) * 305;
            const zureY = Math.floor(i / 2) * 200;
            if (checked) {
                this.SpriteStrC(PN_zmDHHntTxt + i, SCol.Yel + SWCol.Blk + "✓", 0,
                    810 + zureX, 139 + zureY + 168);
            } else {
                this.SpriteStrC(PN_zmDHHntTxt + i, "★" + db.hScene[i].hint, 16,
                    810 + zureX, 139 + zureY + 168);
            }
        }
    };

    const _MenuZukanTatieDetailBtnDraw = Game_Interpreter.prototype.MenuZukanTatieDetailBtnDraw;
    Game_Interpreter.prototype.MenuZukanTatieDetailBtnDraw = function () {
        if (!client || !client.slot_data.randomize_yariman_encyclopedia) 
            return _MenuZukanTatieDetailBtnDraw.call(this);

        _ensureZukanEntry(viewDetailID - 1);
        return _MenuZukanTatieDetailBtnDraw.call(this);
    };

    const _Menu_ZukanTextDraw = Game_Interpreter.prototype.Menu_ZukanTextDraw;
    Game_Interpreter.prototype.Menu_ZukanTextDraw = function (zukanData, yId) {
        _Menu_ZukanTextDraw.call(this, zukanData, yId);
        if (!client || !client.slot_data.randomize_yariman_encyclopedia) return;
        // Entries once gotten have the hint of "look". This hides the hint and shows the full stats.
        // We want both the hint and full stats so we stash it as _realHint and draw the hint ourselves.
        if (Zukan_YarimanFlg && zukanData.cProfile.hint === "look" && zukanData._realHint) {
            this.SetSpriteFIn(PN_zmDHint, mZukan_PicPath + "PN_zmHint", BPs._x, BPs._y, 0, 0, 5);
            this.SpriteStr(PN_zmDHintTxt, zukanData._realHint, 20, 698, 225, 0);
            this.MoveSprite(PN_zmDHintTxt, true, true, 5);
        }
    };
    // #endregion

    // #region Event Patching
    const eventPatches = [];
    let eventPatchLoadingMapId = null;
    let _handlerCounter = 0;

    const EVENT_DUMMY_CMD = Object.freeze({ code: 0, indent: 0, parameters: [] });

    function _registerHandler(fn) {
        _handlerCounter += 1;
        const key = `__yarimono_ap_patch_${_handlerCounter}`;
        window[key] = fn;
        return key;
    }

    
    function _scriptCallCmd(handlerKey, indent) {
        return {
            code: 355,
            indent: indent | 0, // When replacing an existing command or inserting within an indented block make sure to preserve indentation..
            parameters: [`window.${handlerKey}(this._mapId, this._eventId);`],
        };
    }

    function _toRegex(strOrRegex) {
        if (strOrRegex instanceof RegExp) return strOrRegex;
        const escaped = String(strOrRegex).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        return new RegExp(escaped);
    }

    /**
     * Common matchers for event commands. Each matcher returns a function that takes a command and returns true if it matches.
     */
    const Match = {
        /** Matches a script command whose first parameter matches the given string or regex. */
        script(strOrRegex) {
            const regex = _toRegex(strOrRegex);
            return (cmd) => cmd.code === 355
                && cmd.parameters && typeof cmd.parameters[0] === 'string'
                && regex.test(cmd.parameters[0]);
        },
        /** Matches any command with the given code. */
        command(code) {
            return (cmd) => cmd.code === code;
        },
        /** Matches a command with the given code and at least one string parameter that matches the given string or regex. */
        commandWithText(code, strOrRegex) {
            const regex = _toRegex(strOrRegex);
            return (cmd) => cmd.code === code
                && Array.isArray(cmd.parameters)
                && cmd.parameters.some(param => typeof param === 'string' && regex.test(param));
        },
        /** Matches a dialogue command (code 401) whose first parameter matches the given string or regex. */
        dialogue(strOrRegex) {
            const regex = _toRegex(strOrRegex);
            return (cmd) => cmd.code === 401
                && cmd.parameters && typeof cmd.parameters[0] === 'string'
                && regex.test(cmd.parameters[0]);
        },
        /** Matches any command that matches at least one of the given matchers. */
        any(...matchers) { return (cmd) => matchers.some(m => m(cmd)); },
        /** Matches any command that matches all of the given matchers. */
        all(...matchers) { return (cmd) => matchers.every(m => m(cmd)); },
    };

    /** Replaces each matching command with a script call to `handler`. */
    function replaceMatching(matcher, handler) {
        const key = _registerHandler(handler);
        return (list, _ctx) => {
            for (let i = 0; i < list.length; i++) {
                if (matcher(list[i])) list[i] = _scriptCallCmd(key, list[i].indent);
            }
        };
    }

    /** Drop matching commands entirely (no handler dispatched). */
    function removeMatching(matcher) {
        return (list, _ctx) => list.filter(cmd => !matcher(cmd));
    }

    /** 
     * Replace the entire event list with a call to `handler`.
     * If this is a map event, also add a code 0 command because lists
     * with only one event don't run?
     */
    function replaceEntire(handler) {
        const key = _registerHandler(handler);
        return (_list, ctx) => ctx.kind === 'map'
            ? [_scriptCallCmd(key), EVENT_DUMMY_CMD]
            : [_scriptCallCmd(key)];
    }

    /**
     * Replace text in dialogue commands (code 401) that matches `matcher` with
     * `newText`. If `newText` is an array, each entry becomes its own 401.
     */
    function replaceDialogue(matcher, newText) {
        const texts = Array.isArray(newText) ? newText : [newText];
        return (list, _ctx) => {
            let changed = false;
            const out = [];
            for (const cmd of list) {
                if (cmd.code === 401 && typeof cmd.parameters[0] === 'string' && matcher(cmd)) {
                    changed = true;
                    for (const t of texts) {
                        out.push(Object.assign({}, cmd, { parameters: [t] }));
                    }
                } else {
                    out.push(cmd);
                }
            }
            return changed ? out : undefined;
        };
    }

    /** Insert a script call that runs `handler` just before each matching command. */
    function insertBeforeMatching(matcher, handler) {
        const key = _registerHandler(handler);
        return (list, _ctx) => {
            let changed = false;
            const out = [];
            for (const cmd of list) {
                if (matcher(cmd)) {
                    out.push(_scriptCallCmd(key, cmd.indent));
                    changed = true;
                }
                out.push(cmd);
            }
            return changed ? out : undefined;
        };
    }

    /**
     * Insert a script call to `handler` immediately before the Show Text (101)
     * header that owns the matched 401 line. 
     */
    function insertBeforeMessageOf(matcher, handler) {
        const key = _registerHandler(handler);
        return (list, _ctx) => {
            const insertAt = new Set();
            for (let i = 0; i < list.length; i++) {
                if (!matcher(list[i])) continue;
                let j = i - 1;
                while (j >= 0 && list[j].code !== 101) j--;
                insertAt.add(j >= 0 ? j : i);
            }
            if (insertAt.size === 0) return undefined;
            const out = [];
            for (let i = 0; i < list.length; i++) {
                if (insertAt.has(i)) out.push(_scriptCallCmd(key, list[i].indent));
                out.push(list[i]);
            }
            return out;
        };
    }

    /**
     * Replace a dialogue line and run `handler` right before it shows. The
     * handler typically does `$gameVariables.setValue(N, ...)` so `newText`
     * can interpolate via `\V[N]`.
     */
    function replaceDialogueWith(matcher, newText, handler) {
        return compose(
            insertBeforeMessageOf(matcher, handler),
            replaceDialogue(matcher, newText),
        );
    }

    /** Run several transforms sequentially over the same list. */
    function compose(...transforms) {
        return (list, ctx) => {
            let current = list;
            for (const t of transforms) {
                const out = t(current, ctx);
                if (Array.isArray(out)) current = out;
            }
            return current === list ? undefined : current;
        };
    }

    /**
     * Define a patch to apply to a common event or map event page.
     * @param {object} spec - The patch specification.
     * @param {object} spec.target - The target of the patch, either { commonEventId } or { mapId, eventId }.
     * @param {number[]} [spec.pages] - For map events, the page indices to apply the patch to. If omitted, applies to all pages.
     * @param {function} spec.transform - The transform function to apply to the event list. Takes (list, ctx) and returns a new list or modifies in place. Context has shape { kind: 'common', commonEventId } or { kind: 'map', mapId, eventId, pageIndex }.
     */
    function defineEventPatch(spec) {
        if (!spec || typeof spec.transform !== 'function') {
            throw new Error('defineEventPatch needs { target, transform }');
        }
        const t = spec.target || {};
        let target;
        if (t.commonEventId != null) {
            target = { kind: 'common', commonEventId: t.commonEventId };
        } else if (t.templateEventId != null) {
            target = { kind: 'template', templateEventId: t.templateEventId };
        } else if (t.mapId != null && t.eventId != null) {
            target = { kind: 'map', mapId: t.mapId, eventId: t.eventId };
        } else {
            throw new Error('defineEventPatch target needs commonEventId, templateEventId, or {mapId, eventId}');
        }
        eventPatches.push({
            target,
            pages: spec.pages,
            transform: spec.transform,
        });
    }

    // Run a transform against `owner.list` (a CE or a map-event page). If the
    // transform returns a new array, swap it in; otherwise assume in-place mutation.
    function _applyTransform(owner, transform, ctx) {
        const out = transform(owner.list, ctx);
        if (Array.isArray(out)) owner.list = out;
    }

    /**
     * Apply patches to common events. Should be called after loading common 
     * event data, and will modify the common events in-place.
     */
    function applyCommonEventPatches() {
        if (!$dataCommonEvents) return;
        for (const patch of eventPatches) {
            if (patch.target.kind !== 'common') continue;
            const commonEvent = $dataCommonEvents[patch.target.commonEventId];
            if (!commonEvent) continue;
            _applyTransform(commonEvent, patch.transform, {
                kind: 'common',
                commonEventId: patch.target.commonEventId,
            });
        }
    }

    /**
     * Apply patches to template events ($dataTemplateEvents, populated at boot
     * by the EventTemplate plugin from Map 1). Should be called once after
     * connect — template events live forever and aren't reloaded.
     */
    function applyTemplatePatches() {
        if (typeof $dataTemplateEvents === 'undefined' || !$dataTemplateEvents) return;
        for (const patch of eventPatches) {
            if (patch.target.kind !== 'template') continue;
            const templateEvent = $dataTemplateEvents[patch.target.templateEventId];
            if (!templateEvent || !templateEvent.pages) continue;
            const pageIdxs = patch.pages || templateEvent.pages.map((_, i) => i);
            for (const pi of pageIdxs) {
                const page = templateEvent.pages[pi];
                if (!page) continue;
                _applyTransform(page, patch.transform, {
                    kind: 'template',
                    templateEventId: patch.target.templateEventId,
                    pageIndex: pi,
                });
            }
        }
    }

    /**
     * Apply patches to map events on the given map. Should be called after loading
     * map data, and will modify the map events in-place.
     * @param {number} mapId - The ID of the map we are patching events for. Only patches targeting this map will be applied.
     */
    function applyMapPatches(mapId) {
        if (mapId == null || !$dataMap || !$dataMap.events) return;
        for (const patch of eventPatches) {
            if (patch.target.kind !== 'map' || patch.target.mapId !== mapId) continue;
            const event = $dataMap.events[patch.target.eventId];
            if (!event || !event.pages) continue;
            const pageIdxs = patch.pages || event.pages.map((_, i) => i);
            for (const pi of pageIdxs) {
                const page = event.pages[pi];
                if (!page) continue;
                _applyTransform(page, patch.transform, {
                    kind: 'map',
                    mapId: patch.target.mapId,
                    eventId: patch.target.eventId,
                    pageIndex: pi,
                });
            }
        }
    }

    
    // To know what map we're loading when loading map data, so we can apply patches to the right map events in onLoad.
    const _DataManager_loadMapData = DataManager.loadMapData;
    DataManager.loadMapData = function (mapId) {
        eventPatchLoadingMapId = mapId > 0 ? mapId : null;
        _DataManager_loadMapData.call(this, mapId);
    };


    // Apply patches after loading common events or map data.
    const _DataManager_onLoad = DataManager.onLoad;
    DataManager.onLoad = function (object) {
        _DataManager_onLoad.call(this, object);
        if (!client) return;
        if (object === $dataCommonEvents) {
            applyCommonEventPatches();
        } else if (object === $dataMap && eventPatchLoadingMapId != null) {
            applyMapPatches(eventPatchLoadingMapId);
        }
    };

    // Snapshots of original event lists, so we can restore if needed.
    const _originalCEListSnapshots = new Map();

    /**
     * Save a copy of the original command list for a common event, so we can restore or
     * run the original later if needed. Does nothing if we've already saved a snapshot for this CE.
     * @param {number} ceId - The ID of the common event to snapshot.
     */
    function snapshotCEList(ceId) {
        if (_originalCEListSnapshots.has(ceId)) return;
        const ce = $dataCommonEvents && $dataCommonEvents[ceId];
        if (ce && ce.list) {
            _originalCEListSnapshots.set(ceId, ce.list.slice());
        }
    }

    /**
     * Restore all common events to their original command lists.
     */
    function restoreAllCEs() {
        for (const [ceId, originalList] of _originalCEListSnapshots) {
            const ce = $dataCommonEvents && $dataCommonEvents[ceId];
            if (ce) ce.list = originalList.slice();
        }
    }
    // #endregion

    // #region Define Event Patches
    const TRAINER_LV_UP = Match.script('$gameSystem.TrainerLv++');

    // 10th Jizo Level (CE 68)
    defineEventPatch({
        target: { commonEventId: 68 },
        transform: replaceMatching(TRAINER_LV_UP, () => {
            if (client) client.sendLocationChecks([JIZO_SET_COMPLETE_LOC_ID]);
        }),
    });
    // Jizo conversation 10 (TE 1363) dialogue patch
    defineEventPatch({
        target: { templateEventId: 1363 },
        transform: compose(
            replaceDialogue(
                Match.dialogue("Isn't it about time you leveled up!?"),
                "Isn't it about time you got something good!?"
            ),
            replaceDialogueWith(
                Match.dialogue("Trainer level increased by 1!"),
                "You got a \\V[61].",
                () => {
                    $gameVariables.setValue(61, resolveItemName(JIZO_SET_COMPLETE_LOC_ID));
                }
            )
        ),
    });

    // ED triple level grant (M 170 E 10). Three TrainerLv++ in a row → three checks.
    // Has no dialog to patch.
    let edSetupTick = 0;
    defineEventPatch({
        target: { mapId: 170, eventId: 10 },
        transform: replaceMatching(TRAINER_LV_UP, () => {
            if (!client) return;
            const ids = [
                ED_SETUP_LEVEL_1_LOC_ID,
                ED_SETUP_LEVEL_2_LOC_ID,
                ED_SETUP_LEVEL_3_LOC_ID,
            ];
            client.sendLocationChecks([ids[edSetupTick++ % ids.length]]);
        }),
    });

    // Misc inline TrainerLv++ on specific map events.
    const INLINE_TRAINERLV_CALLSITES = {
        "20:14": {
            locId: MUSHROOM_LEVEL_CITY_ROAD_LOC_ID,
            match: "your Trainer Level goes up",
            replace: "You got a \\V[61]!",
        },
        "36:58": {
            locId: MUSHROOM_LEVEL_CENTRAL_ROAD_LOC_ID,
            match: "your Trainer Level goes up",
            replace: "You got a \\V[61]!",
        },
        "165:10": {
            locId: MENS_BATH_LEVEL_LOC_ID,
            match: "Trainer Level went up by 1",
            replace: "You got a \\V[61]!",
        },
        "17:24": {
            locId: LEO_BIG_CITY_LOC_ID,
            match: "Thanks to Leo's practical advice",
            replace: ["Thanks to Leo's practical advice,", "you got a \\V[61]!"],
            alsoRemove: "level increased by one despite",
        },
    };
    for (const [coords, spec] of Object.entries(INLINE_TRAINERLV_CALLSITES)) {
        const [mapId, eventId] = coords.split(':').map(Number);
        const { locId, match, replace, alsoRemove } = spec;
        const steps = [
            replaceMatching(TRAINER_LV_UP, () => {
                if (client) client.sendLocationChecks([locId]);
            }),
            replaceDialogueWith(
                Match.dialogue(match),
                replace,
                () => { $gameVariables.setValue(61, resolveItemName(locId)); },
            ),
        ];
        if (alsoRemove) steps.push(removeMatching(Match.dialogue(alsoRemove)));
        defineEventPatch({
            target: { mapId, eventId },
            transform: compose(...steps),
        });
    }

    // CE 626 is the shared mushroom level-up trigger. The map caller identifies which one.
    const MUSHROOM_CALLSITES = {
        "18:19":  MUSHROOM_LEVEL_HAJIME_ROAD_LOC_ID,
        "23:67":  MUSHROOM_LEVEL_WANO_VILLAGE_LOC_ID,
        "33:89":  MUSHROOM_LEVEL_HARBOR_TOWN_LOC_ID,
        "73:6":   MUSHROOM_LEVEL_LAVA_HIDEOUT_LOC_ID,
        "74:4":   MUSHROOM_LEVEL_INLET_HIDEOUT_LOC_ID,
        "79:5":   MUSHROOM_LEVEL_FOREST_HIDEOUT_LOC_ID,
        "168:6":  MUSHROOM_LEVEL_SECRET_SHOP_LOC_ID,
    };

    defineEventPatch({
        target: { commonEventId: 626 },
        transform: compose(
            replaceMatching(TRAINER_LV_UP, (mapId, eventId) => {
                let locId = MUSHROOM_CALLSITES[`${mapId}:${eventId}`];
                if (!locId) {
                    warn(`CE 626 grant from unknown callsite Map${mapId} Ev${eventId}`);
                    return;
                }
                // Secret shop sells two mushrooms gated sequentially — disambiguate by purchase order.
                let secretShopMushroomCount = SaveStorage.get($gameSystem, 'secretShopMushroomCount') || 0;
                if (locId === MUSHROOM_LEVEL_SECRET_SHOP_LOC_ID) locId += secretShopMushroomCount++;
                SaveStorage.set($gameSystem, 'secretShopMushroomCount', secretShopMushroomCount);
                if (client) client.sendLocationChecks([locId]);
            }),
            replaceDialogue(
                Match.dialogue("It's a mushroom with a dangerous scent. The trainer's"), 
                "It's a mushroom with a dangerous scent. You're super"
            ),
            replaceDialogueWith(
                Match.dialogue("level has gone up by 1! You're super lucky to find one!"),
                ["lucky to find one!", "You got a \\V[61]."],
                (mapId, eventId) => {
                    if (!client) return;
                    const locId = MUSHROOM_CALLSITES[`${mapId}:${eventId}`];
                    $gameVariables.setValue(61, resolveItemName(locId));
                }
            )
        ),
    });

    // CE 676 is a shared chest open scene. Displays dialog and plays a sound effect. We reuse
    // it for opening chests that are AP locations.
    function _showChestOpenCutscene(apItemName, count = 1) {
        $gameVariables.setValue(61, apItemName);
        $gameVariables.setValue(69, count);
        const list = _originalCEListSnapshots.get(676);
        if (!list) {
            warn("Couldn't find original command list for CE 676 to show chest open cutscene");
            return;
        }
        $gameMap._interpreter.setupChild(list, 0);
    }

    const CHEST_CALLSITES = {
        // (mapId:eventId) → AP location id
        "17:49":  PICKUP_CHEST_BIG_CITY_STAR_DISK_LOC_ID,
        "17:78":  PICKUP_CHEST_BIG_CITY_CASTELLA_LOC_ID,
        "18:26":  PICKUP_CHEST_HAJIME_ROAD_LOC_ID,
        "19:13":  PICKUP_CHEST_CAVE_ROAD_LOC_ID,
        "25:1":   PICKUP_CHEST_WANO_CAVE_1F_ATTACK_LOC_ID,
        "25:15":  PICKUP_CHEST_WANO_CAVE_1F_SOUP_LOC_ID,
        "25:16":  PICKUP_CHEST_WANO_CAVE_1F_CASTLA_LOC_ID,
        "27:7":   PICKUP_CHEST_WANO_CAVE_B1F_SOUP_LOC_ID,
        "33:103": PICKUP_CHEST_HARBOR_TOWN_MUSHROOM_LOC_ID,
        "33:104": PICKUP_CHEST_HARBOR_TOWN_SOUP_LOC_ID,
        "36:7":   PICKUP_CHEST_CENTRAL_ROAD_SOUP_LOC_ID,
        "43:3":   PICKUP_HIDDEN_BASEMENT_INCENSE_LOC_ID,
        "43:5":   PICKUP_HIDDEN_BASEMENT_DETERGENT_LOC_ID,
        "63:7":   PICKUP_CHEST_HOLY_ROAD_LOC_ID,
        "78:6":   PICKUP_CHEST_CONSTRUCTION_OFFICE_LOC_ID,
        "214:13": PICKUP_CHEST_SAND_AREA_1_LOC_ID,
        "214:14": PICKUP_CHEST_SAND_AREA_2_LOC_ID,
        "215:43": PICKUP_CHEST_COASTLINE_LOC_ID,
    };

    // Replace CE 676 with a version that shows our own text.
    defineEventPatch({
        target: { commonEventId: 676 },
        transform: replaceEntire((mapId, eventId) => {
            const locId = CHEST_CALLSITES[`${mapId}:${eventId}`];
            if (!locId) {
                warn(`CE 676 chest open at unknown callsite Map${mapId} Ev${eventId}`);
                return;
            }
            _showChestOpenCutscene(resolveItemName(locId));
            if (client) client.sendLocationChecks([locId]);
        }),
    });

    // Strip the inline Change Items (command 126) from each chest
    for (const coords of Object.keys(CHEST_CALLSITES)) {
        const [mapId, eventId] = coords.split(':').map(Number);
        defineEventPatch({
            target: { mapId, eventId },
            transform: removeMatching(Match.command(126)),
        });
    }

    // Hidden money pickups. We reuse the chest open dialog CE.
    const HIDDEN_GOLD_CALLSITES = {
        "17:190": PICKUP_HIDDEN_BIG_CITY_5000_LOC_ID,
        "33:74":  PICKUP_HIDDEN_HARBOR_TOWN_5000_LOC_ID,
    };
    for (const [coords, locId] of Object.entries(HIDDEN_GOLD_CALLSITES)) {
        const [mapId, eventId] = coords.split(':').map(Number);
        defineEventPatch({
            target: { mapId, eventId },
            transform: replaceEntire(() => {
                if (!client) return;
                _showChestOpenCutscene(resolveItemName(locId));
                client.sendLocationChecks([locId]);
                const key = [$gameMap.mapId(), $gameMap._interpreter._eventId, 'A'];
                $gameSelfSwitches.setValue(key, true);
            }),
        });
    }

    // VIP Card given by Maki. On M 32 E 42.
    // A few dialog lines to replace.
    defineEventPatch({
        target: { mapId: 32, eventId: 42 },
        transform: compose(
            replaceMatching(Match.command(126), (mapId, eventId) => {
                if (!client) return;
                const locId = VIP_CARD_LOC_ID;
                client.sendLocationChecks([locId]);
            }),
            replaceDialogue(
                Match.dialogue('(I received some kind of black card.)'),
                '(I received some kind of item.)'
            ),
            replaceDialogue(Match.dialogue("...She's gone. But this black card... "), 
                "(...She's gone. But this item...)"
            ),
            replaceDialogue(Match.dialogue('Is this a membership card...?'),
                '(Is this an Archipelago item...?)'
            ),
            // Replace the "Obtained the VIP card" line with the AP item name. The
            // handler runs immediately before the line shows and stashes the item
            // name in variable 61 so \V[61] interpolates.
            replaceDialogueWith(
                Match.dialogue('Obtained the VIP card (highest level). '),
                '(Obtained a \\V[61].)',
                () => {
                    if (!client) return;
                    const locId = VIP_CARD_LOC_ID;
                    $gameVariables.setValue(61, resolveItemName(locId));
                },
            ),
        ),
    });

    // TE 21 is the cutscene right after White God
    defineEventPatch({
        target: { templateEventId: 21 },
        transform: (list, ctx) => {
            // Add into the list a call to our handler that sends the check for beating White God.
            const handlerKey = _registerHandler(() => {
                if (!client) return;
                
                log(`Defeated White God, marking White God checkpoint as checked.`);
                client.sendLocationChecks([LOCATION_IDS.STORY_CHECKPOINT + 0]);

                // If that was to goal, also set state to completed.
                if (client.slot_data.goal === 0) {
                    client.sendGoalComplete();
                }
            });
            const callCmd = _scriptCallCmd(handlerKey);
            return [callCmd, ...list];
        },
    });

    // TE 1224 is the cutscene right after Tama
    defineEventPatch({
        target: { templateEventId: 1224 },
        transform: (list, ctx) => {
            // Add into the list a call to our handler that sends the check for beating Tama.
            const handlerKey = _registerHandler(() => {
                if (!client) return;
                
                log(`Defeated Tama, marking Tama checkpoint as checked.`);
                client.sendLocationChecks([LOCATION_IDS.STORY_CHECKPOINT + 1]);

                // If that was to goal, also set state to completed.
                if (client.slot_data.goal === 2) {
                    client.sendGoalComplete();
                }
            });
            const callCmd = _scriptCallCmd(handlerKey);
            return [callCmd, ...list];
        },
    });

    // Secret Shop Matsutake. M 168 E 10
    defineEventPatch({
        target: { mapId: 168, eventId: 10 },
        transform: compose(
            replaceMatching(Match.command(126), () => {
                if (!client) return;
                const locId = SECRET_SHOP_MATSUTAKE_LOC_ID;
                client.sendLocationChecks([locId]);
            }),
            replaceDialogueWith(
                Match.dialogue("Our new product is Matsutake, "), 
                "Our new product is \\V[61]",
                () => {
                    if (!client) return;
                    const locId = SECRET_SHOP_MATSUTAKE_LOC_ID;
                    $gameVariables.setValue(61, resolveItemName(locId));
                },
            )
        ),
    });

    // Secret Shop Wonderful Spray. M 168, E 11
    defineEventPatch({
        target: { mapId: 168, eventId: 11 },
        transform: compose(
            replaceMatching(Match.command(126), () => {
                if (!client) return;
                const locId = SECRET_SHOP_WONDERFUL_SPRAY_LOC_ID;
                client.sendLocationChecks([locId]);
            }),
            replaceDialogueWith(
                Match.dialogue("Our new product is Fabulous Spray"),
                "Our new product is \\V[61]",
                () => {
                    if (!client) return;
                    const locId = SECRET_SHOP_WONDERFUL_SPRAY_LOC_ID;
                    $gameVariables.setValue(61, resolveItemName(locId));
                },
            ),
            // Remove the switch flip (SW 411) that makes the mizuki scene start after purchase.
            removeMatching(Match.command(121))
        ),
    });

    // Secret Shop Nose Hook. M 168, E 12
    defineEventPatch({
        target: { mapId: 168, eventId: 12 },
        transform: compose(
            replaceMatching(Match.command(126), () => {
                if (!client) return;
                const locId = SECRET_SHOP_NOSE_HOOK_LOC_ID;
                client.sendLocationChecks([locId]);
            }),
            replaceDialogueWith(
                Match.dialogue("Our new product is Nose Hook, "),
                "Our new product is \\V[61]",
                () => {
                    if (!client) return;
                    const locId = SECRET_SHOP_NOSE_HOOK_LOC_ID;
                    $gameVariables.setValue(61, resolveItemName(locId));
                },
            )
        ),
    });

    // Secret Shop Strange Medicine. M 168, E 13
    defineEventPatch({
        target: { mapId: 168, eventId: 13 },
        transform: compose(
            replaceMatching(Match.command(126), () => {
                if (!client) return;
                const locId = SECRET_SHOP_STRANGE_MEDICINE_LOC_ID;
                client.sendLocationChecks([locId]);
            }),
            replaceDialogueWith(
                Match.dialogue("Our new product is Strange Medicine, "),
                "Our new product is \\V[61]",
                () => {
                    if (!client) return;
                    const locId = SECRET_SHOP_STRANGE_MEDICINE_LOC_ID;
                    $gameVariables.setValue(61, resolveItemName(locId));
                },
            )
        ),
    });

    // Force Nupuryu fight to always be accessible
    defineEventPatch({
        target: { commonEventId: 478 },
        transform: (list, ctx) => {
            // The command we're looking for is a conditional branch (111) that checks the value of V 60 against 1.
            // We want to change it to 9999 so it (basically) always passes and the fight is always accessible.
            const out = [];
            for (const cmd of list) {
                if (cmd.code === 111 && 
                    cmd.parameters[0] === 1 && // Variable
                    cmd.parameters[1] === 60 && // Variable ID 60
                    cmd.parameters[2] === 0 && // Against Constant
                    cmd.parameters[3] === 1 &&  // Constant Value of 1
                    cmd.parameters[4] === 2 // Less than or Equal To
                ) {
                    out.push(Object.assign({}, cmd, { parameters: [1, 60, 0, 9999, 2] }));
                } else {
                    out.push(cmd);
                }
            }
            return out;
        },
    });

    // We need to patch M 150 E 24 to trigger Totori scene 2 on start.
    // This scene is missable based on a dialog choice, so we trigger it early via patch.
    defineEventPatch({
        target: { mapId: 150, eventId: 24 },
        // Insert at start
        transform: (list, ctx)=> {
            if (!client) return;
            // Add a command at the start of the list that sends the location check for Totori scene 2.
            let key = _registerHandler(() => {
                if (!client) return;
                log(`Triggering check for Totori scene 2 at start of M150 E24.`);
                client.sendLocationChecks([TOTORO_SCENE_2_LOC_ID]);
            });
            const callCmd = _scriptCallCmd(key);
            return [callCmd, ...list];
        },
    });
    // #endregion


    // #region Received Items
    /**
     * Handle an item received from Archipelago.
     */
    function handleReceivedItem(item) {
        log(`Handling received item: ${JSON.stringify(item)}`);
        // Different Id ranges have different handling requirements.
        const itemId = item.item;
        if (itemId >= ITEM_IDS.BASE && itemId < ITEM_IDS.EVENT) {
            // Should always be a level up reward. Grant a level up.
            if (itemId === ITEM_IDS.BASE + 1) {
                log("Granting level up for item", itemId);
                $gameSystem.TrainerLv += 1;
            } else {
                warn("Received unknown item with id in level up range:", itemId);
            }
        } else if (itemId >= ITEM_IDS.EVENT && itemId < ITEM_IDS.JUNK) {
            // Event item. Maps to game item id = itemId - ITEM_IDS.EVENT. Just add it to the inventory.
            const gameItemId = itemId - ITEM_IDS.EVENT;
            log(`Adding item ${gameItemId} to inventory for received item ${itemId}`);
            _gameParty_gainItem.call($gameParty, $dataItems[gameItemId], 1);
            // 20000 yen Swimsuit Voucher_Back (53) and Wonderful Spray (57) each require a
            // specific switch to be flipped to actually trigger their event scenes properly.
            if (gameItemId === 53) {
                log("Received Swimsuit Voucher_Back, flipping switch 358 to enable swimsuit scenes.");
                $gameSwitches.setValue(358, true);
                // Can now access Aoi scene without seeing the conversation at the secret shop. That
                // conversation will still happen if you go there though.
            } else if (gameItemId === 57) {
                log("Received Wonderful Spray, flipping switch 411 to enable mizuki scene.");
                // Wonderful Spray scene will now trigger as soon as you enter the secret shop.
                $gameSwitches.setValue(411, true);
            }
        } else if (itemId >= ITEM_IDS.JUNK && itemId < ITEM_IDS.ULTIMATE_MOVE) {
            // Junk item. Maps to game item id = itemId - ITEM_IDS.JUNK. Just add it to the inventory.
            const gameItemId = itemId - ITEM_IDS.JUNK;
            log(`Adding item ${gameItemId} to inventory for received junk item ${itemId}`);
            $gameParty.gainItem($dataItems[gameItemId], 1);
        } else if (itemId >= ITEM_IDS.ULTIMATE_MOVE && itemId < ITEM_IDS.SCENE_UNLOCK) {
            // Ultimate move unlock. Need to flip the relevant switch to unlock it.
            // Switch id = itemId - ITEM_IDS.ULTIMATE_MOVE
            const switchId = itemId - ITEM_IDS.ULTIMATE_MOVE;
            log(`Unlocking ultimate move for switch ${switchId} for received item ${itemId}`);
            $gameSwitches.setValue(switchId, true, true);
        } else if (itemId >= ITEM_IDS.SCENE_UNLOCK) {
            // Scene unlock.
            let { charNo, sceneIndex } = _itemSceneIndex(itemId) || {};
            if (charNo !== undefined && sceneIndex !== undefined) {
                let id = yarimanIdFromGalleryIndex(charNo)
                if (id === null) {
                    warn("Received item with id in scene unlock range but charNo doesn't map to a known gallery id:", item);
                    return;
                }
                unlockScene(charNo, sceneIndex);

            } else {
                warn("Received item with id in scene unlock range but location doesn't map to a known scene:", item);
            }
        }
    }
    // #endregion


    // #region Shops
    const AP_PURCHASE_SLOTS = [
        // Main shops
        { region: "Laboratory",                   cap: 3, label: "Lab Shop",    mapId: 6,  eventId: 5  },
        { region: "Yarimon Center (Big City)",    cap: 1, label: "YC Big City", mapId: 38, eventId: 11 },
        { region: "Yarimon Center (Harbor Town)", cap: 1, label: "YC Harbor",   mapId: 66, eventId: 9  },
        { region: "Big City",                     cap: 2, label: "DS Food A",   mapId: 48, eventId: 8  },
        { region: "Big City",                     cap: 1, label: "DS Food B",   mapId: 48, eventId: 9  },

        // Vending — Hajime Road
        { region: "Hajime Road",  cap: 4, label: "VM Hajime Road A",  mapId: 18, eventId: 27 },
        { region: "Hajime Road",  cap: 3, label: "VM Hajime Road B",  mapId: 18, eventId: 28 },

        // Vending — Cave Road
        { region: "Cave Road",    cap: 3, label: "VM Cave Road A",    mapId: 19, eventId:  6 },
        { region: "Cave Road",    cap: 4, label: "VM Cave Road B",    mapId: 19, eventId:  7 },

        // Vending — Old Road
        { region: "Old Road",     cap: 3, label: "VM Old Road",       mapId: 37, eventId: 20 },

        // Vending — Big City (street-level)
        { region: "Big City",     cap: 3, label: "VM Big City A",     mapId: 17, eventId:  96 },
        { region: "Big City",     cap: 3, label: "VM Big City B",     mapId: 17, eventId:  97 },
        { region: "Big City",     cap: 3, label: "VM Big City C",     mapId: 17, eventId:  98 },
        { region: "Big City",     cap: 4, label: "VM Big City D",     mapId: 17, eventId:  99 },
        { region: "Big City",     cap: 4, label: "VM Big City E",     mapId: 17, eventId: 100 },
        { region: "Big City",     cap: 3, label: "VM Big City F",     mapId: 17, eventId: 101 },
        { region: "Big City",     cap: 3, label: "VM Big City G",     mapId: 17, eventId: 102 },
        { region: "Big City",     cap: 4, label: "VM Big City H",     mapId: 17, eventId: 103 },
        { region: "Big City",     cap: 3, label: "VM Big City I",     mapId: 17, eventId: 104 },

        // Vending — Department Store 2F
        { region: "Big City",     cap: 4, label: "VM Dept Store A",   mapId: 48, eventId: 10 },
        { region: "Big City",     cap: 3, label: "VM Dept Store B",   mapId: 48, eventId: 11 },
        { region: "Big City",     cap: 3, label: "VM Dept Store C",   mapId: 48, eventId: 12 },

        // Vending — Central Church 2F
        { region: "Central Church 2F", cap: 4, label: "VM Church A",  mapId: 84, eventId:  9 },
        { region: "Central Church 2F", cap: 3, label: "VM Church B",  mapId: 84, eventId: 10 },
        { region: "Central Church 2F", cap: 3, label: "VM Church C",  mapId: 84, eventId: 13 },

        // Vending — Beach Road
        { region: "Beach Road",   cap: 4, label: "VM Beach Road",     mapId: 32, eventId: 34 },

        // Vending — Harbor Town
        { region: "Harbor Town",  cap: 3, label: "VM Harbor A",       mapId: 33, eventId: 50 },
        { region: "Harbor Town",  cap: 3, label: "VM Harbor B",       mapId: 33, eventId: 51 },
        { region: "Harbor Town",  cap: 3, label: "VM Harbor C",       mapId: 33, eventId: 52 },
        { region: "Harbor Town",  cap: 3, label: "VM Harbor D",       mapId: 33, eventId: 53 },
        { region: "Harbor Town",  cap: 4, label: "VM Harbor E",       mapId: 33, eventId: 54 },

        // Vending — Resort
        { region: "Resort",       cap: 4, label: "VM Resort A",       mapId: 213, eventId: 33 },
        { region: "Resort",       cap: 4, label: "VM Resort B",       mapId: 213, eventId: 37 },
        { region: "Resort",       cap: 3, label: "VM Resort C",       mapId: 213, eventId: 39 },
        { region: "Resort",       cap: 3, label: "VM Resort D",       mapId: 213, eventId: 46 }
    ];

    // mapId:eventId to label
    const COORDS_TO_SHOP = {}
    for (const slot of AP_PURCHASE_SLOTS) {
        COORDS_TO_SHOP[`${slot.mapId}:${slot.eventId}`] = slot.label;
    }

    let slotsByShop = null
    /**
     * Given the number of extra AP levels, build a mapping of shop label to the list of 
     * AP location ids that should be injected into that shop's inventory.
     */
    function buildShopSlotIndex(extraLevels) {
        const out = {};
        if (extraLevels <= 0) return out;

        let remaining = extraLevels;
        const filled = AP_PURCHASE_SLOTS.map(() => 0);
        let nextId = 0;

        while (remaining > 0) {
            let progress = false;
            for (let i = 0; i < AP_PURCHASE_SLOTS.length && remaining > 0; i++) {
                const slot = AP_PURCHASE_SLOTS[i];
                if (filled[i] >= slot.cap) continue;
                filled[i] += 1;
                (out[slot.label] = out[slot.label] || []).push(LOCATION_IDS.EXTRA_SHOP + nextId);
                nextId += 1;
                remaining -= 1;
                progress = true;
            }
            if (!progress) break;
        }
        return out;
    }

    function apLocIdFromShopItemId(itemId) {
        const offset = itemId - AP_SHOP_ITEM_ID_BASE;
        if (offset < 0) return null;
        return LOCATION_IDS.EXTRA_SHOP + offset;
    }
    function shopItemIdFromApLocId(apId) {
        return AP_SHOP_ITEM_ID_BASE + (apId - LOCATION_IDS.EXTRA_SHOP);
    }
    function apLocIdFromEventShopItemId(itemId) {
        const offset = itemId - EVENT_SHOP_ITEM_ID_BASE;
        if (offset < 0) return null;
        return LOCATION_IDS.EVENT_PURCHASE + offset;
    }
    function eventShopItemIdFromApLocId(apId) {
        const offset = apId - LOCATION_IDS.EVENT_PURCHASE;
        if (offset < 0) return null;
        return EVENT_SHOP_ITEM_ID_BASE + offset;
    }

    // command302 controls opening a shop. We replace it to inject our extra 
    // items into the shop inventory before it opens.
    const _Game_Interpreter_command302 = Game_Interpreter.prototype.command302;
    Game_Interpreter.prototype.command302 = function () {
        const res = _Game_Interpreter_command302.apply(this, arguments);
        if (!client) return res;
        if (!slotsByShop) return res;

        // If any event items exist, replace them with their replacement AP location item.
        // The replacements have an id of + EVENT_SHOP_ITEM_ID_BASE.
        for (let i = 0; i < N_ShopArr.length; i++) {
            const itemId = N_ShopArr[i];
            if (EVENT_SHOP_ITEM_IDS.includes(itemId)) {
                let modifiedItemId = itemId + EVENT_SHOP_ITEM_ID_BASE;
                if (SaveStorage.isLocationChecked($gameSystem, modifiedItemId)) {
                    // Location already checked, remove the item from the shop.
                    N_ShopArr.splice(i, 1);
                    i--;
                } else {
                    // Not checked, replace with the AP location item.
                    N_ShopArr[i] = modifiedItemId + 1 // Game item ids are 1-based.
                }
            }
        }

        const key = `${this._mapId}:${this._eventId}`;
        const label = COORDS_TO_SHOP[key];
        if (!label) return res; // No extra AP items assigned to this shop.

        const apIds = slotsByShop[label];
        if (!apIds || apIds.length === 0) return res;

        let added = 0;
        for (const apId of apIds) {
            if (SaveStorage.isLocationChecked($gameSystem, apId)) continue;
            const itemId = shopItemIdFromApLocId(apId);
            if (!$N_Yarimon_DB.douguDatas[itemId]) {
                warn(`AP shop item ${itemId} not registered (apId=${apId})`);
                continue;
            }
            N_ShopArr.push(itemId + 1); // Game item ids are 1-based.
            added += 1;
        }
        if (added > 0) log(`injected ${added} AP slot(s) into ${label}`);
        return res;
    };
    // #endregion


    // #region Cheat Tackle Limit
    const _Game_Interpreter_PicFrameDraw = Game_Interpreter.prototype.PicFrameDraw;
    Game_Interpreter.prototype.PicFrameDraw = function () {
        let res = _Game_Interpreter_PicFrameDraw.apply(this, arguments);
        if (!client) return res;
        if (client.slot_data.limited_cheat_tackle === 0) return res;
        let cheatTackleLimit = (client.slot_data.limited_cheat_tackle || 0) + (SaveStorage.get($gameSystem, "cheatTackleLimitBonus") || 0);
        this.SpriteStrC( PN_ExAtkCount , " Ex Attack Count " + $gameVariables.value(VN_ExAtkCount) + "/" + cheatTackleLimit + " ", 10 , 720 , 778);
        return res;
    }

    /**
     * Checks if the cheat tackle limit has been reached based on the current count and the limit from slot data.
     */
    function cheatTackleLimitReached() {
        if (!client) return false;
        if (client.slot_data.limited_cheat_tackle === 0) return false;
        let cheatTackleLimit = (client.slot_data.limited_cheat_tackle || 0) + (SaveStorage.get($gameSystem, "cheatTackleLimitBonus") || 0);
        return $gameVariables.value(VN_ExAtkCount) >= cheatTackleLimit;
    }

    const _Game_Interpreter_BtlSelect_Tatakau_Update = Game_Interpreter.prototype.BtlSelect_Tatakau_Update;
    Game_Interpreter.prototype.BtlSelect_Tatakau_Update = function (ckMode) {
        if (!client) return _Game_Interpreter_BtlSelect_Tatakau_Update.call(this, ckMode);
        if (cheatTackleLimitReached()) {
            if (Input.isTriggered('ok')) {
                PlayerUseWazaData = battle_Class.plYarimons[battle_Class.PLMonNo].btlWazas[ckMode.selecterNo];
                if (PlayerUseWazaData.id === WazaID._チートタックル || PlayerUseWazaData.id === WazaID._未来への翼) {
                    return // Eat the input and do nothing, preventing the move from being used.
                }
            }
        }
        return _Game_Interpreter_BtlSelect_Tatakau_Update.call(this, ckMode);
    }

    /**
     * Counts the number of unlocked scenes in the gallery by iterating through the gallery data 
     * in $gameSystem.mZukan and summing up the hSceneFlg arrays.
     */
    function countUnlockedScenes() {
        let count = 0;
        for (let i = 0; i <= $N_Yariman_DB.length - 1; i++) {
            if ($gameSystem.mZukan[i] && $gameSystem.mZukan[i].hSceneFlg) {
                for (let j = 0; j < $gameSystem.mZukan[i].hSceneFlg.length; j++) {
                    if ($gameSystem.mZukan[i].hSceneFlg[j]) {
                        count += 1;
                    }
                }
            }
        }
        return count;
    }

    /** Recalculates the cheat tackle bonus based on unlocked scenes and encyclopedia bonus. */
    function recalculateCheatTackleBonus() {
        if (!client) return;
        if (client.slot_data.encyclopedia_ct_bonus && client.slot_data.limited_cheat_tackle > 0) {
            let totalCount = countUnlockedScenes();
            let newCheatTackleLimitBonus = Math.floor(totalCount / client.slot_data.encyclopedia_ct_bonus);
            SaveStorage.set($gameSystem,"cheatTackleLimitBonus", newCheatTackleLimitBonus);
            // Redraw UI
            PicFrame_ReDrawFlg = true;
            log(`Incremented unlocked scenes count to ${totalCount} and cheat tackle limit to ${newCheatTackleLimitBonus}`);
        }
    }
    // #endregion
    
    // #region Game Data Initialization
    /**
     * Initializes game data like adding items and applying patches to events.
     */
    function gameDataInitialization() {
        // This function is run after connecting to Archipelago on either a new game or loaded save.

        // Trigger patching of common events. Snapshot them in case we need to revert.
        for (const spec of eventPatches) {
            if (spec.target.kind === 'common') snapshotCEList(spec.target.commonEventId);
        }
        applyCommonEventPatches();
        applyTemplatePatches();
        // The current map might have been loaded before we connected, so apply map patches if so.
        if ($gameMap && $gameMap.mapId()) applyMapPatches($gameMap.mapId());


        // Set look flags on gallery so all characters can be viewed without needing to unlock them in-game.
        for (let i = 0; i <= $N_Yariman_DB.length - 1; i++) {
            if ($gameSystem.mZukan[i]) {
                $gameSystem.mZukan[i].lookFlg = true;
            }
        }

        // Add items to shops for each extra level we have from AP.
        addShopItemsToDatabase();

        // Calculate the cheat tackle bonus based on unlocked scenes. In case we have some scenes
        // already unlocked from a previous session.
        recalculateCheatTackleBonus();

        // The postgame has an odd system where some trainers levels are set entirely based on the
        // player's trainer level. We want them to have a proper recommended and minimum level. The
        // game actually has this logic, but doesn't use it for most trainers for some reason. This
        // adds in reasonable numbers for all of them.
        for (const { id, suisyoLv, trLvHikakuMinLv } of trainerRecLevelAdjustments) {
            if ($N_Yarimon_DB.trainers[id]) {
                $N_Yarimon_DB.trainers[id].suisyoLv = suisyoLv; // Recommended level
                $N_Yarimon_DB.trainers[id].trLvHikakuMinLv = trLvHikakuMinLv; // Minimum level
            }
        }
    }

    // apLocId -> NetworkItem (populated by LocationScouts response).
    let scoutedItems = {};

    
    /**
     * Adds extra items to the item database that will be injected into shops to represent AP locations.
     * An item is added for each extra level as well as for each event item in the normal game.
     */
    function addShopItemsToDatabase() {
        let num = client.slot_data.extra_levels
        let rng = makeRng(client.slot_data.seed + 1);
        // Item data is stored in $N_Yarimon_DB.douguDatas. We need to add extra items to it starting at id 100
        // (to avoid conflicts with real items) for each extra level we have, so that they can be added to shops.
        function createItemData(id) {
            return {
                bunrui: "大切",
                exSkillList: [],
                id,
                name: `AP Item ${id}`,
                name_Locs: [
                    { locName: "en", value: `AP Item ${id}` },
                    { locName: "cn", value: `AP Item ${id}` },
                    { locName: "tc", value: `AP Item ${id}` },
                    { locName: "ko", value: `AP Item ${id}` },
                ],
                notSyohiFlg: false,
                picPath: "archipelago",
                price: 1000 * (1 + Math.floor(rng() * 10)), // Random price between 1000 and 10000
                setu: "An item from Archipelago",
                setu_Locs: [
                    { locName: "en", value: "An item from Archipelago" },
                    { locName: "cn", value: "An item from Archipelago" },
                    { locName: "tc", value: "An item from Archipelago" },
                    { locName: "ko", value: "An item from Archipelago" },
                ],
            };
        }
        for (let i = 0; i < num; i++) {
            const id = AP_SHOP_ITEM_ID_BASE + i;
            if (!$N_Yarimon_DB.douguDatas[id]) {
                $N_Yarimon_DB.douguDatas[id] = createItemData(id);
            }
        }
        for (const num of EVENT_SHOP_ITEM_IDS) {
            let id = EVENT_SHOP_ITEM_ID_BASE + num;
            if (!$N_Yarimon_DB.douguDatas[id]) {
                $N_Yarimon_DB.douguDatas[id] = createItemData(id);
            }
        }

        // Attempt to update immediately, just in case we already have the data.
        updateShopItemNames();
    }

    /**
     * Updates the names and descriptions of the shop items based on the scouted item data
     * from the server, so that they have proper readable names.
     */
    function updateShopItemNames() {
        if (!client) return;
        const num = (client.slot_data && client.slot_data.extra_levels) | 0;
        if (num <= 0) return;
        let labelled = 0;
        function updateNameForItem(itemId, apLocId) {
            const entry = $N_Yarimon_DB.douguDatas[itemId];
            if (!entry) return;
            const networkItem = scoutedItems[apLocId];
            if (!networkItem) return;

            // Item lives in the receiving player's game data package.
            const itemName = client.itemName(networkItem.player, networkItem.item);
            const recipient = client.playerName(networkItem.player);
            const isSelf = networkItem.player === (client.slotInfo && client.slotInfo.slot);
            const displayName = isSelf ? itemName : `${itemName} (${recipient})`;
            const desc = isSelf
                ? `Archipelago: ${itemName}`
                : `Archipelago: ${itemName} for ${recipient}`;

            entry.name = displayName;
            for (const loc of entry.name_Locs || []) loc.value = displayName;
            entry.setu = desc;
            for (const loc of entry.setu_Locs || []) loc.value = desc;
            labelled += 1;
        }   
        for (let i = 0; i < num; i++) {
            const itemId = AP_SHOP_ITEM_ID_BASE + i;
            const apLocId = apLocIdFromShopItemId(itemId);
            updateNameForItem(itemId, apLocId);
        }
        for (const num of EVENT_SHOP_ITEM_IDS) {
            const itemId = EVENT_SHOP_ITEM_ID_BASE + num;
            const apLocId = apLocIdFromEventShopItemId(itemId);
            updateNameForItem(itemId, apLocId);
        }
        if (labelled > 0) log(`labelled ${labelled} AP shop slot(s)`);
    }
    // #endregion


    // #region Archipelago Client Initialization
    async function initialize(newGame = false) {
        log("initializing");
        while (!client) {
            const result = await promptInput(
                "Enter Archipelago connection details:",
                [
                    { name: "Host:Port", type: "text",     value: SaveStorage.get($gameSystem, 'hostPort') || '' },
                    { name: "Password",  type: "password", value: Storage.get('password') || '' },
                    { name: "Slot Name", type: "text",     value: SaveStorage.get($gameSystem, 'slot')     || '' },
                ],
                { buttons: [
                    { label: 'Cancel',  cancel: true  },
                    { label: 'Connect', primary: true },
                ]}
            );
            if (result.values === null) {
                log("connect prompt cancelled");
                if (newGame) {
                    // Start a new-non archipelago save.
                    return;
                } else {
                    // Archipelago save in offline mode.
                    // Set an unconnected client so that the rest of the plugin
                    // works properly. Checks will be tracked and resent if they
                    // connect later when loading this save.
                    client = new APClient({ offline: true });
                    addClientListeners(client);
                    gameDataInitialization();
                    showToast("Started in offline mode.", { variant: 'info' });
                    return;
                }
            }
            
            if (newGame && !SaveStorage.isAPSave($gameSystem)) {
                log("marking save as AP save");
                SaveStorage.markAPSave($gameSystem);
            }

            const [host, password, slot] = result.values;
            SaveStorage.set($gameSystem, 'hostPort', host);
            Storage.set('password', password);
            SaveStorage.set($gameSystem, 'slot',     slot);

            const candidate = new APClient({
                host, slot, password,
                uuid: SaveStorage.get($gameSystem, 'uuid') || uuid4(),
            });
            SaveStorage.set($gameSystem, 'uuid', candidate.uuid);

            addClientListeners(candidate);

            try {
                showToast("Connecting to Archipelago...", { variant: 'info' });
                await candidate.connect();
                let savedSeed = SaveStorage.get($gameSystem, 'seed');
                if (candidate.roomInfo && candidate.roomInfo.seed) {
                    if (savedSeed && savedSeed !== candidate.roomInfo.seed) {
                        error(`Seed mismatch. Connected to seed ${candidate.roomInfo.seed} but save file has seed ${savedSeed}`);
                        showToast(`Attempted to connect to a different seed (${candidate.roomInfo.seed}) than the one saved in this save file (${savedSeed}). Connection aborted.`, { variant: 'error', ms: 10000 });
                        candidate.close();
                        return;
                    }
                    if (!savedSeed) {
                        SaveStorage.set($gameSystem, 'seed', candidate.roomInfo.seed);
                        log(`saved seed ${candidate.roomInfo.seed} to save file`);
                    }
                }
                log("connected to Archipelago as slot:", slot);
                showToast(`Connected as ${slot}`, { variant: 'success' });
                client = candidate;
                gameDataInitialization();
            } catch (e) {
                error("connect failed:", e);
                showToast(`Connection failed: ${e.message}`, { variant: 'error', ms: 5000 });
            }
        }

    }

    function addClientListeners(c) {
        c.on("itemReceived", ({ index, item }) => {
            log(`item #${index}: ap_item_id=${item.item} from location=${item.location} player=${item.player}`);
            handleReceivedItem(item);
        });
        c.on("print", (msg) => {
            const ourSlot = c.slotInfo && c.slotInfo.slot;
            if (msg.type === 'ItemSend' || msg.type === 'ItemCheat') {
                // Items we receive are toasted by handleReceivedItem. Other
                // players' item traffic isn't relevant.
                const sender = msg.item && msg.item.player;
                if (sender !== ourSlot || msg.receiving === ourSlot) return;
            }
            const data = Array.isArray(msg.data) ? msg.data : [];
            const text = data.map(seg => (seg && typeof seg.text === 'string') ? seg.text : '').join('');
            if (!text) return;
            log("server:", text);
            const variant = (msg.type === 'Goal' || msg.type === 'Release')         ? 'success'
                          : (msg.type === 'CommandResult' && /error/i.test(text))   ? 'error'
                          : 'info';
            showToast(text, { variant, ms: 6000 });
        });
        c.on("disconnected", ({ code }) => {
            log(`disconnected from Archipelago (code=${code})`);
            showToast(`Disconnected (code=${code})`, { variant: 'error' });
        });
        c.on("connected", (msg) => {
            const extraLevels = (msg.slot_data && msg.slot_data.extra_levels) | 0;
            slotsByShop = buildShopSlotIndex(extraLevels);
        });
        c.on("connected", () => {
            if (!c._hasConnectedOnce) {
                // So we don't catch the initial connection.
                c._hasConnectedOnce = true;
                return;
            }
            log("reconnected to Archipelago");
            showToast("Archipelago reconnected", { variant: 'success', ms: 1500 });
        });
        c.on("locationInfo", (msg) => {
            if (!msg || !Array.isArray(msg.locations)) return;
            for (const it of msg.locations) {
                if (it && typeof it.location === 'number') {
                    scoutedItems[it.location] = it;
                }
            }
            SaveStorage.set($gameSystem, 'offlineScoutedItems', scoutedItems);
            updateShopItemNames();
        });
        c.on("dataPackageReady", () => {
            updateShopItemNames();
        });
    }
    // #endregion
    

    // New game is started by transfering to the opening cutscene map and we're
    // coming from the title screen.
    const _Player_performTransfer = Game_Player.prototype.performTransfer;
    Game_Player.prototype.performTransfer = function () {
        const newGame = this.newMapId() === OPENING_CUTSCENE_MAP_ID && $gameMap.mapId() === MENU_MAP_ID;
        log(`Performing transfer from map ${$gameMap.mapId()} to ${this.newMapId()}`);
        if (newGame) {
            _preInit = true; // So we know we need to wait for FirstPlayerSetting to run before handling items.
            // Initialize Archipelago.
            initialize(true).catch((e) => error("initialize threw:", e));
        }
        return _Player_performTransfer.apply(this, arguments);
    };
    
    // Existing save loaded. Only initialize Archipelago if this is an AP save
    const _loadGame = DataManager.loadGame;
    DataManager.loadGame = function (saveFileId) {
        let res = _loadGame.call(this, saveFileId);
        log(`Save ${saveFileId} loaded, checking for Archipelago data...`);
        if (SaveStorage.isAPSave($gameSystem)) {
            // Initialize Archipelago.
            initialize().catch((e) => error("initialize threw:", e));
        }
        return res;
    };

    showToast("Yarimono Archipelago plugin loaded.", { variant: 'info' });
})();