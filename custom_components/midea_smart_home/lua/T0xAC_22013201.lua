local bit = require "bit".bit
local JSON = require "cjson"
local keyT = {}
keyT["KEY_VERSION"] = "version"
keyT["KEY_POWER"] = "power"
keyT["KEY_PURIFIER"] = "purifier"
keyT["KEY_MODE"] = "mode"
keyT["KEY_SMART_DRY"] = "smart_dry_value"
keyT["KEY_TEMPERATURE"] = "temperature"
keyT["KEY_FANSPEED"] = "wind_speed"
keyT["KEY_SWING_LR"] = "wind_swing_lr"
keyT["KEY_SWING_UD"] = "wind_swing_ud"
keyT["KEY_SWING_LR_UNDER"] = "wind_swing_lr_under"
keyT["KEY_TIME_ON"] = "power_on_timer"
keyT["KEY_TIME_OFF"] = "power_off_timer"
keyT["KEY_CLOSE_TIME"] = "power_off_time_value"
keyT["KEY_OPEN_TIME"] = "power_on_time_value"
keyT["KEY_ECO"] = "eco"
keyT["KEY_DRY"] = "dry"
keyT["KEY_PTC"] = "ptc"
keyT["KEY_CURRENT_WORK_TIME"] = "current_work_time"
keyT["KEY_ERROR_CODE"] = "error_code"
keyT["KEY_BUZZER"] = "buzzer"
keyT["KEY_PREVENT_SUPER_COOL"] = "prevent_super_cool"
keyT["KEY_PREVENT_COLD"] = "prevent_cold"
keyT["KEY_PREVENT_STRAIGHT_WIND"] = "prevent_straight_wind"
keyT["KEY_AUTO_PREVENT_STRAIGHT_WIND"] = "auto_prevent_straight_wind"
keyT["KEY_SELF_CLEAN"] = "self_clean"
keyT["KEY_WIND_STRAIGHT"] = "wind_straight"
keyT["KEY_WIND_AVOID"] = "wind_avoid"
keyT["KEY_INTELLIGENT_WIND"] = "intelligent_wind"
keyT["KEY_NO_WIND_SENSE"] = "no_wind_sense"
keyT["KEY_FN_NO_WIND_SENSE"] = "fn_no_wind_sense"
keyT["KEY_CHILD_PREVENT_COLD_WIND"] = "child_prevent_cold_wind"
keyT["KEY_STRONG_WIND"] = "strong_wind"
keyT["KEY_COMFORT_POWER_SAVE"] = "comfort_power_save"
keyT["KEY_SCREEN_DISPLAY"] = "screen_display"
keyT["KEY_SCREEN_DISPLAY_NOW"] = "screen_display_now"
keyT["KEY_LITTLE_ANGLE"] = "little_angel"
keyT["KEY_COOL_HOT_SENSE"] = "cool_hot_sense"
keyT["KEY_GENTLE_WIND_SENSE"] = "gentle_wind_sense"
keyT["KEY_SECURITY"] = "security"
keyT["KEY_EVEN_WIND"] = "even_wind"
keyT["KEY_SINGLE_TUYERE"] = "single_tuyere"
keyT["KEY_EXTREME_WIND"] = "extreme_wind"
keyT["KEY_VOICE_CONTROL"] = "voice_control"
keyT["KEY_COMFORT_SLEEP"] = "comfort_sleep"
keyT["KEY_COMFORT_SLEEP_CURVE"] = "comfort_sleep_curve"
keyT["KEY_PRE_COOL_HOT"] = "pre_cool_hot"
keyT["KEY_NATURAL_WIND"] = "natural_wind"
keyT["KEY_PMV"] = "pmv"
keyT["KEY_WATER_WASHING"] = "water_washing"
keyT["KEY_FRESH_AIR"] = "fresh_air"
keyT["KEY_YB_WIND_AVOID"] = "yb_wind_avoid"
keyT["KEY_FA_PREVENT_STRAIGHT_WIND"] = "fa_prevent_straight_wind"
keyT["KEY_PARENT_CONTROL"] = "parent_control"
keyT["KEY_NOBODY_ENERGY_SAVE"] = "nobody_energy_save"
keyT["KEY_WIND_SWING_UD_ANGLE"] = "wind_swing_ud_angle"
keyT["KEY_WIND_SWING_LR_ANGLE"] = "wind_swing_lr_angle"
keyT["KEY_FILTER_VALUE"] = "filter_value"
keyT["KEY_FILTER_LEVEL"] = "filter_level"
keyT["KEY_PREVENT_STRAIGHT_WIND_LR"] = "prevent_straight_wind_lr"
keyT["KEY_PM25_VALUE"] = "pm25_value"
keyT["KEY_WATER_PUMP"] = "water_pump"
keyT["KEY_INTENLLIGENT_CONTROL"] = "intelligent_control"
keyT["KEY_VOLUME_CONTROL"] = "volume_control"
keyT["KEY_VOICE_CONTROL_NEW"] = "voice_control_new"
keyT["KEY_FACE_REGISTER"] = "face_register"
keyT["KEY_COOL_TEMP_UP"] = "cool_temp_up"
keyT["KEY_COOL_TEMP_DOWN"] = "cool_temp_down"
keyT["KEY_AUTO_TEMP_UP"] = "auto_temp_up"
keyT["KEY_AUTO_TEMP_DOWN"] = "auto_temp_down"
keyT["KEY_HEAT_TEMP_UP"] = "heat_temp_up"
keyT["KEY_HEAT_TEMP_DOWN"] = "heat_temp_down"
keyT["KEY_POWER_SAVING"] = "power_saving"
keyT["KEY_POWER_LOCK"] = "power_lock"
keyT["KEY_PTC_LOCK"] = "ptc_lock"
keyT["KEY_OFFLINE_OPERATING_TIME"] = "offline_operating_time"
keyT["KEY_REMOTE_CONTROL_LOCK"] = "remote_control_lock"
keyT["KEY_OPERATING_TIME"] = "operating_time"
keyT["KEY_FRESH_FILTER_TIME_TOTAL"] = "fresh_filter_time_total"
keyT["KEY_FRESH_FILTER_TIME_USE"] = "fresh_filter_time_use"
keyT["KEY_FRESH_FILTER_TIMEOUT"] = "fresh_filter_timeout"
keyT["KEY_FRESH_FILTER_RESET"] = "fresh_filter_reset"
keyT["KEY_INDOOR_HUMIDITY"] = "indoor_humidity"
keyT["KEY_DEGERMING"] = "degerming"
keyT["KEY_WIND_AROUND"] = "wind_around"
keyT["KEY_WIND_TOP"] = "wind_top"
keyT["KEY_CHILD_LOCK"] = "child_lock"
local keyV = {}
keyV["VALUE_VERSION"] = 18
keyV["VALUE_FUNCTION_ON"] = "on"
keyV["VALUE_FUNCTION_OFF"] = "off"
keyV["VALUE_MODE_HEAT"] = "heat"
keyV["VALUE_MODE_COOL"] = "cool"
keyV["VALUE_MODE_AUTO"] = "auto"
keyV["VALUE_MODE_DRY"] = "dry"
keyV["VALUE_MODE_FAN"] = "fan"
keyV["VALUE_MODE_SMART_DRY"] = "smart_dry"
keyV["VALUE_INDOOR_TEMPERATURE"] = "indoor_temperature"
keyV["VALUE_OUTDOOR_TEMPERATURE"] = "outdoor_temperature"
keyV["VALUE_RUN_STATE"] = "runstate"
keyV["VALUE_RUNNING"] = "running"
keyV["VALUE_STOP"] = "stopped"
local deviceSubType = 0
local deviceSN8 = "00000000"
local keyB = {}
keyB["BYTE_DEVICE_TYPE"] = 0xAC
keyB["BYTE_CONTROL_REQUEST"] = 0x02
keyB["BYTE_QUERYL_REQUEST"] = 0x03
keyB["BYTE_PROTOCOL_HEAD"] = 0xAA
keyB["BYTE_PROTOCOL_LENGTH"] = 0x0A
keyB["BYTE_POWER_ON"] = 0x01
keyB["BYTE_POWER_OFF"] = 0x00
keyB["BYTE_MODE_AUTO"] = 1
keyB["BYTE_MODE_COOL"] = 2
keyB["BYTE_MODE_DRY"] = 3
keyB["BYTE_MODE_HEAT"] = 4
keyB["BYTE_MODE_FAN"] = 5
keyB["BYTE_MODE_SMART_DRY"] = 6
keyB["BYTE_FANSPEED_AUTO"] = 0x66
keyB["BYTE_FANSPEED_HIGH"] = 0x50
keyB["BYTE_FANSPEED_MID"] = 0x3C
keyB["BYTE_FANSPEED_LOW"] = 0x28
keyB["BYTE_FANSPEED_MUTE"] = 0x14
keyB["BYTE_PURIFIER_ON"] = 0x20
keyB["BYTE_PURIFIER_OFF"] = 0x00
keyB["BYTE_ECO_ON"] = 0x80
keyB["BYTE_ECO_OFF"] = 0x00
keyB["BYTE_SWING_LR_ON"] = 1
keyB["BYTE_SWING_LR_OFF"] = 0
keyB["BYTE_SWING_LR_UNDER_ON"] = 0x80
keyB["BYTE_SWING_LR_UNDER_OFF"] = 0x00
keyB["BYTE_SWING_LR_UNDER_ENABLE"] = 0x80
keyB["BYTE_SWING_LR_UNDER_DISABLE"] = 0x00
keyB["BYTE_SWING_UD_ON"] = 1
keyB["BYTE_SWING_UD_OFF"] = 0
keyB["BYTE_DRY_ON"] = 0x01
keyB["BYTE_DRY_OFF"] = 0x00
keyB["BYTE_BUZZER_ON"] = 0x40
keyB["BYTE_BUZZER_OFF"] = 0x00
keyB["BYTE_CONTROL_CMD"] = 0x40
keyB["BYTE_TIMER_METHOD_REL"] = 0x00
keyB["BYTE_TIMER_METHOD_ABS"] = 0x01
keyB["BYTE_TIMER_METHOD_DISABLE"] = 0x7F
keyB["BYTE_CLIENT_MODE_MOBILE"] = 0x02
keyB["BYTE_TIMER_SWITCH_ON"] = 0x80
keyB["BYTE_TIMER_SWITCH_OFF"] = 0x00
keyB["BYTE_CLOSE_TIMER_SWITCH_ON"] = 0x80
keyB["BYTE_CLOSE_TIMER_SWITCH_OFF"] = 0x7F
keyB["BYTE_START_TIMER_SWITCH_ON"] = 0x80
keyB["BYTE_START_TIMER_SWITCH_OFF"] = 0x7F
keyB["BYTE_PTC_ON"] = 0x08
keyB["BYTE_PTC_OFF"] = 0x00
keyB["BYTE_STRONG_WIND_ON"] = 0x20
keyB["BYTE_STRONG_WIND_OFF"] = 0x00
keyB["BYTE_SLEEP_ON"] = 0x03
keyB["BYTE_SLEEP_OFF"] = 0x00
keyB["BYTE_COMFORT_POWER_SAVE_ON"] = 0x01
keyB["BYTE_COMFORT_POWER_SAVE_OFF"] = 0x00
keyB["BYTE_EVEN_WIND_ON"] = 0x01
keyB["BYTE_EVEN_WIND_OFF"] = 0x00
keyB["BYTE_SINGLE_TUYERE_ON"] = 0x01
keyB["BYTE_SINGLE_TUYERE_OFF"] = 0x00
keyB["BYTE_EXTREME_WIND_ON"] = 0x01
keyB["BYTE_EXTREME_WIND_OFF"] = 0x00
keyB["BYTE_VOICE_CONTROL_ON"] = 0x03
keyB["BYTE_VOICE_CONTROL_OFF"] = 0x00
keyB["BYTE_NATURAL_WIND_ON"] = 0x40
keyB["BYTE_NATURAL_WIND_OFF"] = 0x00
keyB["BYTE_CONTROL_PROPERTY_CMD"] = 0xB0
local keyP = {}
local dataType = 0
local comfortByte = nil
local tempControl = 0
local function init_keyP()
    keyP["is_query"] = nil
    keyP["timerSignal"] = 0
    keyP["powerValue"] = nil
    keyP["modeValue"] = nil
    keyP["smartDryValue"] = nil
    keyP["temperature"] = nil
    keyP["smallTemperature"] = nil
    keyP["indoorTemperatureValue"] = nil
    keyP["smallIndoorTemperatureValue"] = nil
    keyP["outdoorTemperatureValue"] = nil
    keyP["smallOutdoorTemperatureValue"] = nil
    keyP["fanspeedValue"] = nil
    keyP["closeTimerSwitch"] = nil
    keyP["openTimerSwitch"] = nil
    keyP["closeHour"] = nil
    keyP["closeStepMintues"] = nil
    keyP["closeMin"] = nil
    keyP["closeTime"] = nil
    keyP["openHour"] = nil
    keyP["openStepMintues"] = nil
    keyP["openMin"] = nil
    keyP["openTime"] = nil
    keyP["strongWindValue"] = nil
    keyP["comfortableSleepValue"] = nil
    keyP["comfortableSleepSwitch"] = nil
    keyP["comfortableSleepTime"] = nil
    keyP["comfort_sleep_curve"] = nil
    keyP["PTCValue"] = nil
    keyP["purifierValue"] = nil
    keyP["ecoValue"] = nil
    keyP["dryValue"] = nil
    keyP["swingLRValue"] = nil
    keyP["swingUDValue"] = nil
    keyP["swingLRValueUnder"] = nil
    keyP["swingLRUnderSwitch"] = 0
    keyP["currentWorkTime"] = nil
    keyP["PTCForceValue"] = 0
    keyP["screenDisplayNowValue"] = nil
    keyP["buzzerValue"] = 0x40
    keyP["errorCode"] = 0
    keyP["kickQuilt"] = nil
    keyP["preventCold"] = nil
    keyP["comfortPowerSave"] = nil
    keyP["naturalWind"] = nil
    keyP["pmv"] = nil
    keyP["fresh_filter_time_total"] = nil
    keyP["fresh_filter_time_use"] = nil
    keyP["fresh_filter_timeout"] = nil
    keyP["fresh_filter_reset"] = nil
    keyP["propertyNumber"] = 0
    keyP["prevent_super_cool"] = nil
    keyP["prevent_straight_wind"] = nil
    keyP["auto_prevent_straight_wind"] = nil
    keyP["self_clean"] = nil
    keyP["wind_straight"] = nil
    keyP["wind_avoid"] = nil
    keyP["yb_wind_avoid"] = nil
    keyP["intelligent_wind"] = nil
    keyP["no_wind_sense"] = nil
    keyP["child_prevent_cold_wind"] = nil
    keyP["little_angel"] = nil
    keyP["cool_hot_sense"] = nil
    keyP["gentle_wind_sense"] = nil
    keyP["security"] = nil
    keyP["even_wind"] = nil
    keyP["single_tuyere"] = nil
    keyP["extreme_wind"] = nil
    keyP["extreme_wind_level"] = nil
    keyP["voice_control"] = nil
    keyP["pre_cool_hot"] = nil
    keyP["water_washing"] = nil
    keyP["fresh_air"] = nil
    keyP["no_wind_sense_level"] = nil
    keyP["fn_no_wind_sense"] = nil
    keyP["fa_prevent_straight_wind"] = nil
    keyP["parent_control"] = nil
    keyP["parent_control_temp_up"] = nil
    keyP["parent_control_temp_down"] = nil
    keyP["nobody_energy_save"] = nil
    keyP["filter_value"] = nil
    keyP["filter_level"] = nil
    keyP["prevent_straight_wind_lr"] = nil
    keyP["pm25_value"] = nil
    keyP["water_pump"] = nil
    keyP["intelligent_control"] = nil
    keyP["wind_swing_ud_angle"] = nil
    keyP["wind_swing_lr_angle"] = nil
    keyP["volume_control"] = nil
    keyP["voice_control_new"] = nil
    keyP["face_register"] = nil
    keyP["cool_temp_up"] = nil
    keyP["cool_temp_down"] = nil
    keyP["auto_temp_up"] = nil
    keyP["auto_temp_down"] = nil
    keyP["heat_temp_up"] = nil
    keyP["heat_temp_down"] = nil
    keyP["power_saving"] = nil
    keyP["remote_control_lock"] = nil
    keyP["remote_control_lock_control"] = nil
    -- keyP["indoor_humidity"] = nil  -- preserve C1/0x45 value across messages
    keyP["degerming"] = nil
    keyP["wind_around"] = nil
    keyP["wind_around_ud"] = nil
    keyP["wind_top"] = nil
    keyP["light"] = nil
    keyP["child_lock"] = nil
    keyP["electrify_time_day"] = nil
    keyP["electrify_time_hour"] = nil
    keyP["electrify_time_min"] = nil
    keyP["electrify_time_second"] = nil
    keyP["total_operating_time_day"] = nil
    keyP["total_operating_time_hour"] = nil
    keyP["total_operating_time_min"] = nil
    keyP["total_operating_time_second"] = nil
    keyP["current_operating_time_day"] = nil
    keyP["current_operating_time_hour"] = nil
    keyP["current_operating_time_min"] = nil
    keyP["current_operating_time_second"] = nil
    keyP["total_power_consumption"] = nil
    keyP["total_operating_consumption"] = nil
    keyP["current_operating_consumption"] = nil
    keyP["current_time_power"] = nil
    keyP["analysis_value"] = nil
    keyP["filter_replace_time"] = nil
    keyP["dust_full_time"] = nil
    keyP["buzzer_all"] = nil
    keyP["self_remove_odor_phase"] = nil
    keyP["high_temp_remove_odor_alone"] = nil
    keyP["power_lock"] = nil
    keyP["ptc_lock"] = nil
    keyP["offline_operating_time"] = nil
    keyP["ozone"] = nil
    keyP["fault_tag"] = nil
    keyP["soft_warm"] = nil
    keyP["fresh_air_parm"] = nil
    keyP["rewarming_dry"] = nil
    keyP["arom"] = nil
    keyP["arom_old"] = nil
    keyP["arom_fan_speed"] = nil
    keyP["arom_time_clean"] = nil
    keyP["arom_time"] = nil
    keyP["arom_time_total"] = nil
    keyP["new_mode_power"] = nil
    keyP["new_mode"] = nil
    keyP["new_temperature"] = nil
    keyP["new_wind_speed"] = nil
    keyP["uvc_remove_odor"] = nil
    keyP["uvc_power_off"] = nil
    keyP["main_horizontal_guide_strip_1"] = nil
    keyP["main_horizontal_guide_strip_2"] = nil
    keyP["main_horizontal_guide_strip_3"] = nil
    keyP["main_horizontal_guide_strip_4"] = nil
    keyP["has_guide_strip"] = nil
    keyP["has_no_wind_sense"] = nil
    keyP["has_arom"] = nil
    keyP["light_sensitive"] = nil
    keyP["t2_temp"] = nil
    keyP["wind_swing_lr_left"] = nil
    keyP["wind_swing_lr_right"] = nil
    keyP["wind_swing_ud_left"] = nil
    keyP["wind_swing_ud_right"] = nil
    keyP["whirl_wind_left"] = nil
    keyP["whirl_wind_right"] = nil
    keyP["inner_purifier"] = nil
    keyP["inner_purifier_fan_speed"] = nil
    keyP["inner_purifier_mode"] = nil
    keyP["wind_speed_right"] = nil
    keyP["fresh_air_mode_two"] = nil
    keyP["indoor_co2"] = nil
    keyP["humidification"] = nil
    keyP["humidification_fan_speed"] = nil
    keyP["humidification_mode"] = nil
    keyP["remove_odor"] = nil
    keyP["remove_odor_fan_speed"] = nil
    keyP["fresh_air_on_co2"] = nil
    keyP["fresh_air_off_co2"] = nil
    keyP["gentle_wind_enable"] = nil
    keyP["linkage"] = nil
    keyP["moisturizing"] = nil
    keyP["moisturizing_fan_speed"] = nil
    keyP["linkage_sync"] = nil
    keyP["ilinkId"] = nil
    keyP["ticket"] = nil
    keyP["temperature_enable"] = 0
    keyP["wind_speed_enable"] = 0
    keyP["power_off_temp_wind"] = 0
    keyP["power_off_total"] = 0
    keyP["no_wind_sense_left"] = nil
    keyP["no_wind_sense_right"] = nil
    keyP["no_wind_sense_control"] = nil
    keyP["ptc_default_rule"] = nil
    keyP["fresh_filter_reset"] = nil
    keyP["five_dimension_mode"] = nil
    keyP["screen_display_time"] = nil
    keyP["total_status_switch"] = nil
    keyP["linkage_fan_speed"] = nil
    keyP["wind_no_linkage"] = nil
    keyP["wait_clean"] = nil
    keyP["self_clean_time"] = nil
    keyP["self_clean_stage"] = nil
    keyP["dry_clean_time"] = nil
    keyP["dry_clean_stage"] = nil
    keyP["ptc_load"] = nil
    keyP["defrosting_load"] = nil
    keyP["no_wind_sense_judge_param"] = nil
    keyP["real_mode"] = nil
    keyP["left_down_real_wind_speed"] = nil
    keyP["right_up_real_wind_speed"] = nil
    keyP["screen_display_select"] = nil
    keyP["left_ud_wind_angle"] = nil
    keyP["up_lr_wind_angle"] = nil
    keyP["swing_lr_under_angle"] = nil
    keyP["right_ud_wind_angle"] = nil
    keyP["left_lr_wind_angle"] = nil
    keyP["right_lr_wind_angle"] = nil
    keyP["wind_swing_lr_under"] = nil
    keyP["wind_swing_ud_angle_up"] = nil
    keyP["wind_swing_ud_angle_down"] = nil
    keyP["app_control_remember_ud"] = nil
    keyP["wind_swing_ud_angle_switch"] = nil
    keyP["wind_swing_lr_angle_up"] = nil
    keyP["wind_swing_lr_angle_down"] = nil
    keyP["app_control_remember_lr"] = nil
    keyP["wind_swing_lr_angle_switch"] = nil
    keyP["has_wind_swing_ud_angle_diy"] = nil
    keyP["has_wind_swing_lr_angle_diy"] = nil
    keyP["has_left_down_real_wind_speed"] = nil
    keyP["no_wind_sense_up"] = nil
    keyP["no_wind_sense_down"] = nil
    keyP["no_wind_sense_updown_control"] = nil
    keyP["auto_prevent_cold_wind"] = nil
    keyP["cool_power_saving"] = nil
    keyP["has_right_ud_wind_angle"] = nil
    keyP["has_no_wind_sense_judge_param"] = nil
    keyP["linkage_2"] = nil
    keyP["has_linkage_2"] = nil
    keyP["quick_cool_heat"] = nil
    keyP["prepare_food"] = nil
    keyP["prepare_food_temp"] = nil
    keyP["prepare_food_fan_speed"] = nil
    keyP["quick_fry"] = nil
    keyP["quick_fry_temp"] = nil
    keyP["quick_fry_fan_speed"] = nil
    keyP["quick_fry_center_point"] = nil
    keyP["quick_fry_angle"] = nil
    keyP["quick_fry_control"] = nil
    keyP["care_mode"] = nil
    keyP["care_mode_lock"] = nil
    keyP["cool_light_color_r"] = nil
    keyP["cool_light_color_g"] = nil
    keyP["cool_light_color_b"] = nil
    keyP["heat_light_color_r"] = nil
    keyP["heat_light_color_g"] = nil
    keyP["heat_light_color_b"] = nil
    keyP["dry_light_color_r"] = nil
    keyP["dry_light_color_g"] = nil
    keyP["dry_light_color_b"] = nil
    keyP["remove_odor_light_color_r"] = nil
    keyP["remove_odor_light_color_g"] = nil
    keyP["remove_odor_light_color_b"] = nil
    keyP["fresh_light_color_r"] = nil
    keyP["fresh_light_color_g"] = nil
    keyP["fresh_light_color_b"] = nil
    keyP["purifier_light_color_r"] = nil
    keyP["purifier_light_color_g"] = nil
    keyP["purifier_light_color_b"] = nil
    keyP["dust_full_time_reset"] = nil
    keyP["circle_fan"] = nil
    keyP["circle_fan_mode"] = nil
    keyP["linkage_2_temp_auto"] = nil
    keyP["linkage_2_wind_auto"] = nil
    keyP["linkage_2_fresh_air_auto"] = nil
    keyP["linkage_2_purifier_auto"] = nil
    keyP["linkage_2_humi_auto"] = nil
    keyP["linkage_2_temp_control_type"] = nil
    keyP["linkage_2_wind_control_type"] = nil
    keyP["linkage_2_fresh_air_control_type"] = nil
    keyP["linkage_2_purifier_control_type"] = nil
    keyP["linkage_2_humi_control_type"] = nil
    keyP["breath_cool"] = nil
    keyP["breath_heat"] = nil
    keyP["breath_remove_odor"] = nil
    keyP["breath_fresh_air"] = nil
    keyP["breath_purifier"] = nil
    keyP["prevent_straight_wind_distance"] = nil
    keyP["auto_prevent_cold_wind_memory"] = nil
    keyP["has_auto_prevent_cold_wind_memory"] = nil
    keyP["buzzer_off_status"] = nil
    keyP["air_remove_odor"] = nil
    keyP["has_moisturizing"] = nil
    keyP["eco_time_status"] = nil
    keyP["eco_time_switch"] = nil
    keyP["eco_time_hour"] = nil
    keyP["eco_time_min"] = nil
    keyP["eco_time_sec"] = nil
    keyP["has_eco_time"] = nil
    keyP["frequency_compensation"] = 0
    keyP["dynamic_temp_compensation"] = 0
    keyP["clean_breath"] = nil
    keyP["clean_breath_level"] = nil
    keyP["remove_odor_fan_speed"] = nil
    keyP["remove_odor_time"] = nil
    keyP["tvoc_level"] = nil
    keyP["health"] = nil
    keyP["remove_arofene_clean"] = nil
    keyP["control_source"] = nil
    keyP["arofene_filter_use_time"] = nil
    keyP["fresh_air_mode"] = nil
    keyP["humidification"] = nil
    keyP["strong_cool"] = nil
    keyP["wet_film_clean"] = nil
    keyP["has_strong_cool"] = nil
end
init_keyP()
local propertyPre = nil
local function print_lua_table(lua_table, indent)
    indent = indent or 0
    for k, v in pairs(lua_table) do
        if type(k) == "string" then k = string.format("%q", k) end
        local szSuffix = ""
        if type(v) == "table" then szSuffix = "{" end
        local szPrefix = string.rep("    ", indent)
        formatting = szPrefix .. "[" .. k .. "]" .. " = " .. szSuffix
        if type(v) == "table" then
            print(formatting)
            print_lua_table(v, indent + 1)
            print(szPrefix .. "},")
        else
            local szValue = ""
            if type(v) == "string" then szValue = string.format("%q", v) else szValue = tostring(v) end
            print(formatting .. szValue .. ",")
        end
    end
end
local function checkBoundary(data, min, max)
    if (not data) then data = 0 end
    data = tonumber(data)
    if (data == nil) then data = 0 end
    if ((data >= min) and (data <= max)) then return data else if (data < min) then return min else return max end end
end
local function table2string(cmd)
    local ret = ""
    local i
    for i = 1, #cmd do ret = ret .. string.char(cmd[i]) end
    return ret
end
local function table2string2(cmd)
    local ret = ""
    local i
    for i = 0, #cmd - 1 do ret = ret .. string.char(cmd[i]) end
    return ret
end
local function string2table(hexstr)
    local tb = {}
    local i = 1
    local j = 1
    for i = 1, #hexstr - 1, 2 do
        local doublebytestr = string.sub(hexstr, i, i + 1)
        tb[j] = tonumber(doublebytestr, 16)
        j = j + 1
    end
    return tb
end
local function numstring2table(hexstr)
    local tb = {}
    local i = 1
    local j = 1
    for i = 1, #hexstr - 1, 2 do
        local doublebytestr = string.sub(hexstr, i, i + 1)
        tb[j] = doublebytestr
        j = j + 1
    end
    return tb
end
local function string2hexstring(str)
    local ret = ""
    for i = 1, #str do ret = ret .. string.format("%02x", str:byte(i)) end
    return ret
end
local function encode(cmd)
    local tb
    if JSON == nil then JSON = require "cjson" end
    tb = JSON.encode(cmd)
    return tb
end
local function decode(cmd)
    local tb
    if JSON == nil then JSON = require "cjson" end
    tb = JSON.decode(cmd)
    return tb
end
local function makeSum(tmpbuf, start_pos, end_pos)
    local resVal = 0
    for si = start_pos, end_pos do
        resVal = resVal + tmpbuf[si]
        if resVal > 0xff then resVal = bit.band(resVal, 0xff) end
    end
    resVal = bit.band(255 - resVal + 1, 0xff)
    return resVal
end
local function splitStrByChar(str, sepChar)
    local splitList = {}
    local pattern = '[^' .. sepChar .. ']+'
    string.gsub(str, pattern, function(w) table.insert(splitList, w) end)
    return splitList
end
local function values(t)
    local i = 0
    return function()
        i = i + 1; return t[i]
    end
end
local crc8_854_table = { 0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65, 157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220, 35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98, 190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255, 70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7, 219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154, 101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36, 248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185, 140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205, 17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80, 175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238, 50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115, 202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139, 87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22, 233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168, 116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53 }
local function crc8_854(dataBuf, start_pos, end_pos)
    local crc = 0
    for si = start_pos, end_pos do
        crc = crc8_854_table[bit.band(bit.bxor(crc, dataBuf[si]), 0xFF) + 1]
        print(dataBuf[si])
    end
    return crc
end
local function bcd2Int(bcd) return (bit.band(0x0F, bit.rshift(bcd, 4))) * 10 + bit.band(0x0F, bcd) end
local function setDefaultValue()
    if (keyP["powerValue"] == nil) then keyP["powerValue"] = keyB["BYTE_POWER_ON"] end
    if (keyP["modeValue"] == nil) then keyP["modeValue"] = keyB["BYTE_MODE_AUTO"] end
    if (keyP["smartDryValue"] == nil) then keyP["smartDryValue"] = 50 end
    if (keyP["temperature"] == nil) then keyP["temperature"] = 26 end
    if (keyP["smallTemperature"] == nil) then keyP["smallTemperature"] = 0 end
    if (keyP["fanspeedValue"] == nil) then keyP["fanspeedValue"] = 102 end
    if (keyP["closeTimerSwitch"] == nil) then keyP["closeTimerSwitch"] = keyB["BYTE_CLOSE_TIMER_SWITCH_OFF"] end
    if (keyP["openTimerSwitch"] == nil) then keyP["openTimerSwitch"] = keyB["BYTE_START_TIMER_SWITCH_OFF"] end
    if (keyP["strongWindValue"] == nil) then keyP["strongWindValue"] = keyB["BYTE_STRONG_WIND_OFF"] end
    if (keyP["comfortableSleepValue"] == nil) then keyP["comfortableSleepValue"] = keyB["BYTE_SLEEP_OFF"] end
    if (keyP["comfortableSleepSwitch"] == nil) then keyP["comfortableSleepSwitch"] = 0x00 end
    if (keyP["comfortableSleepTime"] == nil) then keyP["comfortableSleepTime"] = 0x00 end
    if (keyP["PTCValue"] == nil) then keyP["PTCValue"] = keyB["BYTE_PTC_OFF"] end
    if (keyP["purifierValue"] == nil) then keyP["purifierValue"] = keyB["BYTE_PURIFIER_OFF"] end
    if (keyP["dryValue"] == nil) then keyP["dryValue"] = keyB["BYTE_DRY_OFF"] end
    if (keyP["swingLRValue"] == nil) then keyP["swingLRValue"] = keyB["BYTE_SWING_LR_OFF"] end
    if (keyP["swingUDValue"] == nil) then keyP["swingUDValue"] = keyB["BYTE_SWING_UD_OFF"] end
    if (keyP["preventCold"] == nil) then keyP["preventCold"] = 0x00 end
    if (keyP["power_saving"] == nil) then keyP["power_saving"] = 0x00 end
    if (keyP["gentle_wind_enable"] == nil) then keyP["gentle_wind_enable"] = 0x00 end
end
local function jsonToModel(jsonCmd, jsonType)
    local streams = jsonCmd
    if (jsonType == "control" and streams["power"] ~= nil) then
        if (streams[keyT["KEY_POWER"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["powerValue"] = 0x01 elseif (streams[keyT["KEY_POWER"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["powerValue"] = 0x00 end
        print("power ===")
        print(keyP["powerValue"])
    end
    if (jsonType == "control" and streams["power"] ~= nil) then keyP["propertyNumber"] = keyP["propertyNumber"] + 1 end
    if (jsonType == "control" and (streams["whirl_wind_right"] ~= nil or streams["whirl_wind_left"] ~= nil)) then
        keyP["propertyNumber"] = 1
        tempControl = 1
    end
    if (streams[keyT["KEY_BUZZER"]] == "VALUE_FUNCTION_ON") then keyP["buzzerValue"] = keyB["BYTE_BUZZER_ON"] elseif (streams[keyT["KEY_BUZZER"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["buzzerValue"] =
        keyB["BYTE_BUZZER_OFF"] end
    if (streams["ptc_force"] ~= nil) then if (streams["ptc_force"] == "on") then keyP["PTCForceValue"] = 1 else keyP["PTCForceValue"] = 0 end end
    if (streams[keyT["KEY_PURIFIER"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["purifierValue"] = keyB
        ["BYTE_PURIFIER_ON"] elseif (streams[keyT["KEY_PURIFIER"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["purifierValue"] =
        keyB["BYTE_PURIFIER_OFF"] end
    if (jsonType == "control" and streams["eco"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_ECO"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["ecoValue"] = 0x01 elseif (streams[keyT["KEY_ECO"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["ecoValue"] = 0x00 end
    end
    if (jsonType == "control" and streams["dry"] ~= nil) then if (streams[keyT["KEY_DRY"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["dryValue"] =
            keyB["BYTE_DRY_ON"] elseif (streams[keyT["KEY_DRY"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["dryValue"] =
            keyB["BYTE_DRY_OFF"] end end
    if (jsonType == "control" and streams["dry"] ~= nil) then keyP["propertyNumber"] = keyP["propertyNumber"] + 1 end
    if (jsonType == "control" and streams[keyT["KEY_MODE"]] ~= nil) then
        if (streams[keyT["KEY_MODE"]] == keyV["VALUE_MODE_HEAT"]) then keyP["modeValue"] = keyB["BYTE_MODE_HEAT"] elseif (streams[keyT["KEY_MODE"]] == keyV["VALUE_MODE_COOL"]) then keyP["modeValue"] =
            keyB["BYTE_MODE_COOL"] elseif (streams[keyT["KEY_MODE"]] == keyV["VALUE_MODE_AUTO"]) then keyP["modeValue"] =
            keyB["BYTE_MODE_AUTO"] elseif (streams[keyT["KEY_MODE"]] == keyV["VALUE_MODE_DRY"]) then keyP["modeValue"] =
            keyB["BYTE_MODE_DRY"] elseif (streams[keyT["KEY_MODE"]] == keyV["VALUE_MODE_FAN"]) then keyP["modeValue"] =
            keyB["BYTE_MODE_FAN"] elseif (streams[keyT["KEY_MODE"]] == keyV["VALUE_MODE_SMART_DRY"]) then keyP["modeValue"] =
            keyB["BYTE_MODE_SMART_DRY"] end
        print("mode ===")
        print(keyP["modeValue"])
    end
    if (jsonType == "control" and streams[keyT["KEY_MODE"]] ~= nil) then keyP["propertyNumber"] = keyP["propertyNumber"] +
        1 end
    if (streams[keyT["KEY_SMART_DRY"]] ~= nil) then keyP["smartDryValue"] = checkBoundary(streams[keyT["KEY_SMART_DRY"]],
            30, 101) end
    if (streams[keyT["KEY_NATURAL_WIND"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["naturalWind"] = keyB
        ["BYTE_NATURAL_WIND_ON"] elseif (streams[keyT["KEY_NATURAL_WIND"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["naturalWind"] =
        keyB["BYTE_NATURAL_WIND_OFF"] end
    if (streams[keyT["KEY_PMV"]] ~= nil) then keyP["pmv"] = checkBoundary(streams[keyT["KEY_PMV"]], -3.5, 3) end
    if (jsonType == "control" and streams[keyT["KEY_FANSPEED"]]) then if (streams[keyT["KEY_FANSPEED"]] ~= nil) then keyP["fanspeedValue"] =
            checkBoundary(streams[keyT["KEY_FANSPEED"]], 1, 102) end end
    if (jsonType == "control" and streams[keyT["KEY_FANSPEED"]] ~= nil) then keyP["propertyNumber"] = keyP
        ["propertyNumber"] + 1 end
    if (jsonType == "control" and streams[keyT["KEY_SWING_UD"]] ~= nil) then if (streams[keyT["KEY_SWING_UD"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["swingUDValue"] =
            keyB["BYTE_SWING_UD_ON"] elseif (streams[keyT["KEY_SWING_UD"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["swingUDValue"] =
            keyB["BYTE_SWING_UD_OFF"] end end
    if (jsonType == "control" and streams[keyT["KEY_SWING_UD"]] ~= nil) then keyP["propertyNumber"] = keyP
        ["propertyNumber"] + 1 end
    if (jsonType == "control" and streams["wind_swing_ud_left"] ~= nil) then
        if (streams["wind_swing_ud_left"] == keyV["VALUE_FUNCTION_ON"]) then keyP["wind_swing_ud_left"] = 0x01 elseif (streams["wind_swing_ud_left"] == keyV["VALUE_FUNCTION_OFF"]) then keyP["wind_swing_ud_left"] = 0x00 end
        if (jsonType == "control" and streams["wind_swing_ud_left"] ~= nil) then keyP["propertyNumber"] = keyP
            ["propertyNumber"] + 1 end
    end
    if (jsonType == "control" and streams["wind_swing_ud_right"] ~= nil) then if (streams["wind_swing_ud_right"] == keyV["VALUE_FUNCTION_ON"]) then keyP["wind_swing_ud_right"] = 0x01 elseif (streams["wind_swing_ud_right"] == keyV["VALUE_FUNCTION_OFF"]) then keyP["wind_swing_ud_right"] = 0x00 end end
    if (jsonType == "control" and streams["wind_swing_ud_right"] ~= nil) then keyP["propertyNumber"] = keyP
        ["propertyNumber"] + 1 end
    if (jsonType == "control" and streams[keyT["KEY_SWING_LR"]] ~= nil) then if (streams[keyT["KEY_SWING_LR"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["swingLRValue"] =
            keyB["BYTE_SWING_LR_ON"] elseif (streams[keyT["KEY_SWING_LR"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["swingLRValue"] =
            keyB["BYTE_SWING_LR_OFF"] end end
    if (jsonType == "control" and streams[keyT["KEY_SWING_LR"]] ~= nil) then keyP["propertyNumber"] = keyP
        ["propertyNumber"] + 1 end
    if (jsonType == "control" and streams["wind_swing_lr_left"] ~= nil) then if (streams["wind_swing_lr_left"] == keyV["VALUE_FUNCTION_ON"]) then keyP["wind_swing_lr_left"] = 0x01 elseif (streams["wind_swing_lr_left"] == keyV["VALUE_FUNCTION_OFF"]) then keyP["wind_swing_lr_left"] = 0x00 end end
    if (jsonType == "control" and streams["wind_swing_lr_left"] ~= nil) then keyP["propertyNumber"] = keyP
        ["propertyNumber"] + 1 end
    if (jsonType == "control" and streams["wind_swing_lr_right"] ~= nil) then if (streams["wind_swing_lr_right"] == keyV["VALUE_FUNCTION_ON"]) then keyP["wind_swing_lr_right"] = 0x01 elseif (streams["wind_swing_lr_right"] == keyV["VALUE_FUNCTION_OFF"]) then keyP["wind_swing_lr_right"] = 0x00 end end
    if (jsonType == "control" and streams["wind_swing_lr_right"] ~= nil) then keyP["propertyNumber"] = keyP
        ["propertyNumber"] + 1 end
    if (streams[keyT["KEY_SWING_LR_UNDER"]] == keyV["VALUE_FUNCTION_ON"]) then
        keyP["swingLRUnderSwitch"] = keyB["BYTE_SWING_LR_UNDER_ENABLE"]
        keyP["swingLRValueUnder"] = keyB["BYTE_SWING_LR_UNDER_ON"]
    elseif (streams[keyT["KEY_SWING_LR_UNDER"]] == keyV["VALUE_FUNCTION_OFF"]) then
        keyP["swingLRUnderSwitch"] = keyB["BYTE_SWING_LR_UNDER_ENABLE"]
        keyP["swingLRValueUnder"] = keyB["BYTE_SWING_LR_UNDER_OFF"]
    end
    if (jsonType == "control" and streams["wind_swing_lr_under"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_SWING_LR_UNDER"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["wind_swing_lr_under"] = 1 else keyP["wind_swing_lr_under"] = 0 end
    end
    if (jsonType == "control" and streams[keyT["KEY_TIME_ON"]] ~= nil) then if (streams[keyT["KEY_TIME_ON"]] == keyV["VALUE_FUNCTION_ON"]) then
            keyP["openTimerSwitch"] = 0x01
            if (jsonType == "control") then
                keyP["timerSignal"] = 1
                keyP["propertyNumber"] = keyP["propertyNumber"] + 1
            end
        elseif (streams[keyT["KEY_TIME_ON"]] == keyV["VALUE_FUNCTION_OFF"]) then
            keyP["openTimerSwitch"] = 0x00
            if (jsonType == "control") then
                keyP["timerSignal"] = 1
                keyP["propertyNumber"] = keyP["propertyNumber"] + 1
            end
        end end
    if (jsonType == "control" and streams[keyT["KEY_TIME_OFF"]] ~= nil) then if (streams[keyT["KEY_TIME_OFF"]] == keyV["VALUE_FUNCTION_ON"]) then
            keyP["closeTimerSwitch"] = 0x01
            if (jsonType == "control") then
                keyP["timerSignal"] = 1
                keyP["propertyNumber"] = keyP["propertyNumber"] + 1
            end
        elseif (streams[keyT["KEY_TIME_OFF"]] == keyV["VALUE_FUNCTION_OFF"]) then
            keyP["closeTimerSwitch"] = 0x00
            if (jsonType == "control") then
                keyP["timerSignal"] = 1
                keyP["propertyNumber"] = keyP["propertyNumber"] + 1
            end
        end end
    if (streams[keyT["KEY_CLOSE_TIME"]] ~= nil) then
        keyP["closeTime"] = streams[keyT["KEY_CLOSE_TIME"]]
        keyP["closeHour"] = math.floor(keyP["closeTime"] / 60)
        keyP["closeStepMintues"] = math.floor((keyP["closeTime"] % 60))
    end
    if (streams[keyT["KEY_OPEN_TIME"]] ~= nil) then
        keyP["openTime"] = streams[keyT["KEY_OPEN_TIME"]]
        keyP["openHour"] = math.floor(keyP["openTime"] / 60)
        keyP["openStepMintues"] = math.floor((keyP["openTime"] % 60))
    end
    if (jsonType == "control" and streams[keyT["KEY_COMFORT_SLEEP"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_COMFORT_SLEEP"]] == keyV["VALUE_FUNCTION_ON"]) then
            keyP["comfortableSleepValue"] = 0x01
            keyP["comfortableSleepSwitch"] = 0x40
            keyP["comfortableSleepTime"] = 0x0A
        elseif (streams[keyT["KEY_COMFORT_SLEEP"]] == keyV["VALUE_FUNCTION_OFF"]) then
            keyP["comfortableSleepValue"] = 0x00
            keyP["comfortableSleepSwitch"] = 0x00
            keyP["comfortableSleepTime"] = 0x00
        end
    end
    if (streams[keyT["KEY_COMFORT_SLEEP_CURVE"]] ~= nil) then
        streams[keyT["KEY_COMFORT_SLEEP_CURVE"]] = string.gsub(streams[keyT["KEY_COMFORT_SLEEP_CURVE"]], ",", "")
        comfortByte = numstring2table(streams[keyT["KEY_COMFORT_SLEEP_CURVE"]])
    end
    if (jsonType == "control" and streams[keyT["KEY_PTC"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_PTC"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["PTCValue"] = 0x01 elseif (streams[keyT["KEY_PTC"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["PTCValue"] = 0x00 end
    end
    if (jsonType == "control" and streams["ptc_default_rule"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["ptc_default_rule"] = streams["ptc_default_rule"]
    end
    if (streams[keyT["KEY_STRONG_WIND"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["strongWindValue"] = keyB
        ["BYTE_STRONG_WIND_ON"] elseif (streams[keyT["KEY_STRONG_WIND"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["strongWindValue"] =
        keyB["BYTE_STRONG_WIND_OFF"] end
    if (jsonType == "control" and streams[keyT["KEY_TEMPERATURE"]] ~= nil) then if (streams[keyT["KEY_TEMPERATURE"]] ~= nil) then keyP["temperature"] =
            checkBoundary(streams[keyT["KEY_TEMPERATURE"]], 16, 30) end end
    if (jsonType == "control" and streams[keyT["KEY_TEMPERATURE"]] ~= nil) then keyP["propertyNumber"] = keyP
        ["propertyNumber"] + 1 end
    if (streams["small_temperature"] ~= nil) then keyP["smallTemperature"] = checkBoundary(streams["small_temperature"],
            0, 0.5) end
    if (jsonType == "control" and streams[keyT["KEY_COMFORT_POWER_SAVE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_COMFORT_POWER_SAVE"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["comfortPowerSave"] = 0x01 elseif (streams[keyT["KEY_COMFORT_POWER_SAVE"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["comfortPowerSave"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_PREVENT_SUPER_COOL"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_PREVENT_SUPER_COOL"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["prevent_super_cool"] = 0x01 elseif (streams[keyT["KEY_PREVENT_SUPER_COOL"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["prevent_super_cool"] = 0x00 end
    end
    if (streams[keyT["KEY_PREVENT_COLD"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["preventCold"] = 0x01 elseif (streams[keyT["KEY_PREVENT_COLD"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["preventCold"] = 0x00 end
    if (jsonType == "control" and streams[keyT["KEY_PREVENT_STRAIGHT_WIND"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["prevent_straight_wind"] = checkBoundary(streams[keyT["KEY_PREVENT_STRAIGHT_WIND"]], 0, 3)
    end
    if (jsonType == "control" and streams[keyT["KEY_FA_PREVENT_STRAIGHT_WIND"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["fa_prevent_straight_wind"] = checkBoundary(streams[keyT["KEY_FA_PREVENT_STRAIGHT_WIND"]], 0, 2)
    end
    if (jsonType == "control" and streams[keyT["KEY_AUTO_PREVENT_STRAIGHT_WIND"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_AUTO_PREVENT_STRAIGHT_WIND"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["auto_prevent_straight_wind"] = 0x01 elseif (streams[keyT["KEY_AUTO_PREVENT_STRAIGHT_WIND"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["auto_prevent_straight_wind"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_SELF_CLEAN"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_SELF_CLEAN"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["self_clean"] = 0x01 elseif (streams[keyT["KEY_SELF_CLEAN"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["self_clean"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_WIND_STRAIGHT"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_WIND_STRAIGHT"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["wind_straight"] = 0x01 elseif (streams[keyT["KEY_WIND_STRAIGHT"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["wind_straight"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_WIND_AVOID"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_WIND_AVOID"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["wind_avoid"] = 0x01 elseif (streams[keyT["KEY_WIND_AVOID"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["wind_avoid"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_YB_WIND_AVOID"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_YB_WIND_AVOID"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["yb_wind_avoid"] = 0x02 elseif (streams[keyT["KEY_YB_WIND_AVOID"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["yb_wind_avoid"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_INTELLIGENT_WIND"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_INTELLIGENT_WIND"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["intelligent_wind"] = 0x01 elseif (streams[keyT["KEY_INTELLIGENT_WIND"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["intelligent_wind"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_NO_WIND_SENSE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["no_wind_sense"] = checkBoundary(streams[keyT["KEY_NO_WIND_SENSE"]], 0, 5)
    end
    if (jsonType == "control" and streams[keyT["KEY_FN_NO_WIND_SENSE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_FN_NO_WIND_SENSE"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["fn_no_wind_sense"] = 0x01 elseif (streams[keyT["KEY_FN_NO_WIND_SENSE"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["fn_no_wind_sense"] = 0x00 end
    end
    if (streams["no_wind_sense_level"] ~= nil) then keyP["no_wind_sense_level"] = streams["no_wind_sense_level"] end
    if (jsonType == "control" and streams[keyT["KEY_CHILD_PREVENT_COLD_WIND"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_CHILD_PREVENT_COLD_WIND"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["child_prevent_cold_wind"] = 0x01 elseif (streams[keyT["KEY_CHILD_PREVENT_COLD_WIND"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["child_prevent_cold_wind"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_LITTLE_ANGLE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_LITTLE_ANGLE"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["little_angel"] = 0x01 elseif (streams[keyT["KEY_LITTLE_ANGLE"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["little_angel"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_COOL_HOT_SENSE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_COOL_HOT_SENSE"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["cool_hot_sense"] = 0x01 elseif (streams[keyT["KEY_COOL_HOT_SENSE"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["cool_hot_sense"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_GENTLE_WIND_SENSE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_GENTLE_WIND_SENSE"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["gentle_wind_sense"] = 0x01 elseif (streams[keyT["KEY_GENTLE_WIND_SENSE"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["gentle_wind_sense"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_SECURITY"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_SECURITY"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["security"] = 0x01 elseif (streams[keyT["KEY_SECURITY"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["security"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_EVEN_WIND"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_EVEN_WIND"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["even_wind"] = 0x01 elseif (streams[keyT["KEY_EVEN_WIND"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["even_wind"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_SINGLE_TUYERE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_SINGLE_TUYERE"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["single_tuyere"] = 0x01 elseif (streams[keyT["KEY_SINGLE_TUYERE"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["single_tuyere"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_EXTREME_WIND"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_EXTREME_WIND"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["extreme_wind"] = 0x01 elseif (streams[keyT["KEY_EXTREME_WIND"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["extreme_wind"] = 0x00 end
    end
    if (streams["extreme_wind_level"] ~= nil) then keyP["extreme_wind_level"] = streams["extreme_wind_level"] end
    if (jsonType == "control" and streams[keyT["KEY_VOICE_CONTROL"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_VOICE_CONTROL"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["voice_control"] = 0x03 elseif (streams[keyT["KEY_VOICE_CONTROL"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["voice_control"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_PRE_COOL_HOT"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_PRE_COOL_HOT"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["pre_cool_hot"] = 0x01 elseif (streams[keyT["KEY_PRE_COOL_HOT"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["pre_cool_hot"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_WATER_WASHING"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_WATER_WASHING"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["water_washing"] = 0x01 elseif (streams[keyT["KEY_WATER_WASHING"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["water_washing"] = 0x00 end
    end
    if (streams["water_washing_manual"] ~= nil) then
        keyP["water_washing_manual"] = streams["water_washing_manual"]
        keyP["water_washing_time"] = streams["water_washing_time"]
        keyP["water_washing_stage"] = streams["water_washing_stage"]
    end
    if (jsonType == "control" and streams[keyT["KEY_FRESH_AIR"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_FRESH_AIR"]] == keyV["VALUE_FUNCTION_ON"]) then
            keyP["fresh_air"] = 0x01
            if (streams["fresh_air_mode"] ~= nil and streams["fresh_air_mode"] == 1) then keyP["fresh_air"] = 0x03 end
        elseif (streams[keyT["KEY_FRESH_AIR"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["fresh_air"] = 0x00 end
    end
    if (streams["fresh_air_fan_speed"] ~= nil) then
        keyP["fresh_air_fan_speed"] = streams["fresh_air_fan_speed"]
        keyP["fresh_air_temp"] = streams["fresh_air_temp"]
    end
    if (streams["fresh_air_mode_two"] ~= nil) then keyP["fresh_air_mode_two"] = streams["fresh_air_mode_two"] end
    if (jsonType == "control" and streams[keyT["KEY_PARENT_CONTROL"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_PARENT_CONTROL"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["parent_control"] = 0x01 elseif (streams[keyT["KEY_PARENT_CONTROL"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["parent_control"] = 0x00 end
    end
    if (streams["parent_control_temp_up"] ~= nil or keyP["parent_control_temp_down"] ~= nil) then
        keyP["parent_control_temp_up"] = streams["parent_control_temp_up"]
        keyP["parent_control_temp_down"] = streams["parent_control_temp_down"]
    end
    if (jsonType == "control" and streams[keyT["KEY_NOBODY_ENERGY_SAVE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_NOBODY_ENERGY_SAVE"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["nobody_energy_save"] = 0x01 elseif (streams[keyT["KEY_NOBODY_ENERGY_SAVE"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["nobody_energy_save"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_PREVENT_STRAIGHT_WIND_LR"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["prevent_straight_wind_lr"] = checkBoundary(streams[keyT["KEY_PREVENT_STRAIGHT_WIND_LR"]], 0, 3)
    end
    if (jsonType == "control" and streams[keyT["KEY_PM25_VALUE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["pm25_value"] = streams[keyT["KEY_PM25_VALUE"]]
    end
    if (jsonType == "control" and streams[keyT["KEY_WATER_PUMP"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_WATER_PUMP"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["water_pump"] = 0x01 elseif (streams[keyT["KEY_WATER_PUMP"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["water_pump"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_WIND_SWING_UD_ANGLE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["wind_swing_ud_angle"] = streams["wind_swing_ud_angle"]
    end
    if (jsonType == "control" and streams[keyT["KEY_WIND_SWING_LR_ANGLE"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["wind_swing_lr_angle"] = streams["wind_swing_lr_angle"]
    end
    if (jsonType == "control" and streams[keyT["KEY_INTENLLIGENT_CONTROL"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_INTENLLIGENT_CONTROL"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["intelligent_control"] = 0x01 elseif (streams[keyT["KEY_INTENLLIGENT_CONTROL"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["intelligent_control"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_VOLUME_CONTROL"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["volume_control"] = checkBoundary(streams[keyT["KEY_VOLUME_CONTROL"]], 0, 100)
    end
    if (jsonType == "control" and streams[keyT["KEY_VOICE_CONTROL_NEW"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["voice_control_new"] = checkBoundary(streams[keyT["KEY_VOICE_CONTROL_NEW"]], 0, 3)
    end
    if (jsonType == "control" and (streams[keyT["KEY_AUTO_TEMP_UP"]] ~= nil or streams[keyT["KEY_AUTO_TEMP_DOWN"]] ~= nil or streams[keyT["KEY_COOL_TEMP_UP"]] ~= nil or streams[keyT["KEY_COOL_TEMP_DOWN"]] ~= nil or streams[keyT["KEY_HEAT_TEMP_UP"]] ~= nil or streams[keyT["KEY_HEAT_TEMP_DOWN"]] ~= nil)) then keyP["propertyNumber"] =
        keyP["propertyNumber"] + 1 end
    if (streams["cool_temp_up"] ~= nil) then keyP["cool_temp_up"] = streams["cool_temp_up"] end
    if (streams["cool_temp_down"] ~= nil) then keyP["cool_temp_down"] = streams["cool_temp_down"] end
    if (streams["auto_temp_up"] ~= nil) then keyP["auto_temp_up"] = streams["auto_temp_up"] end
    if (streams["auto_temp_down"] ~= nil) then keyP["auto_temp_down"] = streams["auto_temp_down"] end
    if (streams["heat_temp_up"] ~= nil) then keyP["heat_temp_up"] = streams["heat_temp_up"] end
    if (streams["heat_temp_down"] ~= nil) then keyP["heat_temp_down"] = streams["heat_temp_down"] end
    if (jsonType == "control" and streams[keyT["KEY_POWER_SAVING"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_POWER_SAVING"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["power_saving"] = 0x01 elseif (streams[keyT["KEY_POWER_SAVING"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["power_saving"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_POWER_LOCK"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_POWER_LOCK"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["power_lock"] = 0x01 elseif (streams[keyT["KEY_POWER_LOCK"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["power_lock"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_PTC_LOCK"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_PTC_LOCK"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["ptc_lock"] = 0x01 elseif (streams[keyT["KEY_PTC_LOCK"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["ptc_lock"] = 0x00 end
    end
    if (jsonType == "control" and streams[keyT["KEY_OFFLINE_OPERATING_TIME"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["offline_operating_time"] = streams["offline_operating_time"]
    end
    if (jsonType == "control" and streams[keyT["KEY_REMOTE_CONTROL_LOCK"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["remote_control_lock"] = streams["remote_control_lock"]
        keyP["remote_control_lock_control"] = streams["remote_control_lock_control"]
    end
    if (jsonType == "control" and streams[keyT["KEY_OPERATING_TIME"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["operating_time"] = streams["operating_time"]
    end
    if (jsonType == "control" and streams[keyT["KEY_FRESH_FILTER_RESET"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["fresh_filter_reset"] = streams["fresh_filter_reset"]
    end
    if (jsonType == "control" and streams[keyT["KEY_DEGERMING"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_DEGERMING"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["degerming"] = 0x01 elseif (streams[keyT["KEY_DEGERMING"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["degerming"] = 0x00 end
    end
    if (jsonType == "control" and streams["light"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["light"] = checkBoundary(streams["light"], 0, 100)
    end
    if (jsonType == "control" and streams[keyT["KEY_WIND_AROUND"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_WIND_AROUND"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["wind_around"] = 0x01 elseif (streams[keyT["KEY_WIND_AROUND"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["wind_around"] = 0x00 end
    end
    if (streams["wind_around_ud"] ~= nil) then keyP["wind_around_ud"] = streams["wind_around_ud"] end
    if (jsonType == "control" and streams[keyT["KEY_WIND_TOP"]] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams[keyT["KEY_WIND_TOP"]] == keyV["VALUE_FUNCTION_ON"]) then keyP["wind_top"] = 0x01 elseif (streams[keyT["KEY_WIND_TOP"]] == keyV["VALUE_FUNCTION_OFF"]) then keyP["wind_top"] = 0x00 end
    end
    if (jsonType == "control" and streams["child_lock"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["child_lock"] = streams["child_lock"]
    end
    if (jsonType == "control" and streams["ilinkId"] ~= nil) then keyP["ilinkId"] = streams["ilinkId"] end
    if (jsonType == "control" and streams["ticket"] ~= nil) then keyP["ticket"] = streams["ticket"] end
    if (jsonType == "control" and streams["buzzer_all"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["buzzer_all"] = streams["buzzer_all"]
    end
    if (jsonType == "control" and streams["self_remove_odor_phase"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["self_remove_odor_phase"] = streams["self_remove_odor_phase"]
    end
    if (jsonType == "control" and streams["high_temp_remove_odor_alone"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["high_temp_remove_odor_alone"] = streams["high_temp_remove_odor_alone"]
    end
    if (jsonType == "control" and streams["ozone"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["ozone"] = streams["ozone"]
    end
    if (jsonType == "control" and streams["soft_warm"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["soft_warm"] = streams["soft_warm"]
    end
    if (jsonType == "control" and streams["fresh_air_parm"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["fresh_air_parm"] = streams["fresh_air_parm"]
    end
    if (jsonType == "control" and streams["rewarming_dry"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["rewarming_dry"] = streams["rewarming_dry"]
    end
    if (jsonType == "control" and streams["arom"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["arom"] = streams["arom"]
    end
    if (streams["arom_fan_speed"] ~= nil) then keyP["arom_fan_speed"] = streams["arom_fan_speed"] end
    if (streams["arom_time"] ~= nil) then keyP["arom_time"] = streams["arom_time"] end
    if (streams["arom_time_clean"] ~= nil) then keyP["arom_time_clean"] = streams["arom_time_clean"] end
    if (streams["arom_time_total"] ~= nil) then keyP["arom_time_total"] = streams["arom_time_total"] end
    if (jsonType == "control" and streams["new_mode_power"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["new_mode_power"] = streams["new_mode_power"]
    end
    if (jsonType == "control" and streams["new_mode"] ~= nil) then if (streams["new_mode"] == "auto") then keyP["new_mode"] = 1 elseif (streams["new_mode"] == "cool") then keyP["new_mode"] = 2 elseif (streams["new_mode"] == "dry") then keyP["new_mode"] = 3 elseif (streams["new_mode"] == "heat") then keyP["new_mode"] = 4 elseif (streams["new_mode"] == "fan") then keyP["new_mode"] = 5 else keyP["new_mode"] = 0 end end
    if (jsonType == "control" and streams["new_temperature"] ~= nil) then keyP["new_temperature"] = streams
        ["new_temperature"] * 2 end
    if (jsonType == "control" and streams["new_wind_speed"] ~= nil) then keyP["new_wind_speed"] = streams
        ["new_wind_speed"] end
    if (jsonType == "control" and (streams["uvc_remove_odor"] ~= nil or streams["uvc_power_off"] ~= nil)) then keyP["propertyNumber"] =
        keyP["propertyNumber"] + 1 end
    if (streams["uvc_remove_odor"] ~= nil) then keyP["uvc_remove_odor"] = streams["uvc_remove_odor"] end
    if (streams["uvc_power_off"] ~= nil) then keyP["uvc_power_off"] = streams["uvc_power_off"] end
    if (streams["main_horizontal_guide_strip_1"] ~= nil) then keyP["main_horizontal_guide_strip_1"] = streams
        ["main_horizontal_guide_strip_1"] end
    if (streams["main_horizontal_guide_strip_2"] ~= nil) then keyP["main_horizontal_guide_strip_2"] = streams
        ["main_horizontal_guide_strip_2"] end
    if (streams["main_horizontal_guide_strip_3"] ~= nil) then keyP["main_horizontal_guide_strip_3"] = streams
        ["main_horizontal_guide_strip_3"] end
    if (streams["main_horizontal_guide_strip_4"] ~= nil) then keyP["main_horizontal_guide_strip_4"] = streams
        ["main_horizontal_guide_strip_4"] end
    if (jsonType == "control" and (streams["main_horizontal_guide_strip_1"] ~= nil or streams["main_horizontal_guide_strip_2"] ~= nil or streams["main_horizontal_guide_strip_3"] ~= nil or streams["main_horizontal_guide_strip_4"] ~= nil)) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["main_strip_control"] = 1
    end
    if (jsonType == "control" and streams["light_sensitive"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["light_sensitive"] = streams["light_sensitive"]
    end
    if (jsonType == "control" and streams["screen_display_time"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["screen_display_time"] = streams["screen_display_time"]
    end
    if (jsonType == "control" and streams["total_status_switch"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["total_status_switch"] = streams["total_status_switch"]
    end
    if (streams["whirl_wind_left"] ~= nil) then keyP["whirl_wind_left"] = streams["whirl_wind_left"] end
    if (streams["whirl_wind_right"] ~= nil) then keyP["whirl_wind_right"] = streams["whirl_wind_right"] end
    if (jsonType == "control" and streams["inner_purifier"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams["inner_purifier"] == "on") then keyP["inner_purifier"] = 0x01 else keyP["inner_purifier"] = 0x00 end
    end
    if (streams["inner_purifier_fan_speed"] ~= nil) then keyP["inner_purifier_fan_speed"] = streams
        ["inner_purifier_fan_speed"] end
    if (streams["inner_purifier_mode"] ~= nil) then keyP["inner_purifier_mode"] = streams["inner_purifier_mode"] end
    if (jsonType == "control" and streams["wind_speed_right"] ~= nil) then keyP["wind_speed_right"] = checkBoundary(
        streams["wind_speed_right"], 1, 102) end
    if (jsonType == "control" and streams["wind_speed_right"] ~= nil) then keyP["propertyNumber"] = keyP
        ["propertyNumber"] + 1 end
    if (streams["gentle_wind_enable"] ~= nil) then keyP["gentle_wind_enable"] = streams["gentle_wind_enable"] end
    if (jsonType == "control" and streams["remove_odor"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams["remove_odor"] == keyV["VALUE_FUNCTION_ON"]) then keyP["remove_odor"] = 0x01 elseif (streams["remove_odor"] == keyV["VALUE_FUNCTION_OFF"]) then keyP["remove_odor"] = 0x00 end
    end
    if (streams["remove_odor_fan_speed"] ~= nil) then keyP["remove_odor_fan_speed"] = streams["remove_odor_fan_speed"] end
    if (streams["fresh_air_on_co2"] ~= nil) then keyP["fresh_air_on_co2"] = streams["fresh_air_on_co2"] end
    if (streams["fresh_air_off_co2"] ~= nil) then keyP["fresh_air_off_co2"] = streams["fresh_air_off_co2"] end
    if (jsonType == "control" and (streams["fresh_air_on_co2"] ~= nil or streams["fresh_air_off_co2"] ~= nil)) then keyP["propertyNumber"] =
        keyP["propertyNumber"] + 1 end
    if (jsonType == "control" and streams["linkage"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["linkage"] = streams["linkage"]
    end
    if (jsonType == "control" and streams["moisturizing"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["moisturizing"] = streams["moisturizing"]
    end
    if (streams["moisturizing_fan_speed"] ~= nil) then keyP["moisturizing_fan_speed"] = streams
        ["moisturizing_fan_speed"] end
    if (jsonType == "control" and streams["temperature_enable"] ~= nil) then keyP["temperature_enable"] = streams
        ["temperature_enable"] end
    if (jsonType == "control" and streams["wind_speed_enable"] ~= nil) then keyP["wind_speed_enable"] = streams
        ["wind_speed_enable"] end
    if (jsonType == "control" and streams["power_off_temp_wind"] ~= nil) then keyP["power_off_temp_wind"] = streams
        ["power_off_temp_wind"] end
    if (jsonType == "control" and streams["power_off_purifier"] ~= nil) then keyP["power_off_purifier"] = streams
        ["power_off_purifier"] end
    if (streams["no_wind_sense_left"] ~= nil) then if (streams["no_wind_sense_left"] == keyV["VALUE_FUNCTION_ON"]) then keyP["no_wind_sense_left"] = 0x02 elseif (streams["no_wind_sense_left"] == keyV["VALUE_FUNCTION_OFF"]) then keyP["no_wind_sense_left"] = 0x01 end end
    if (streams["no_wind_sense_right"] ~= nil) then if (streams["no_wind_sense_right"] == keyV["VALUE_FUNCTION_ON"]) then keyP["no_wind_sense_right"] = 0x02 elseif (streams["no_wind_sense_right"] == keyV["VALUE_FUNCTION_OFF"]) then keyP["no_wind_sense_right"] = 0x01 end end
    if (jsonType == "control" and (streams["no_wind_sense_left"] ~= nil or streams["no_wind_sense_right"] ~= nil)) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["no_wind_sense_control"] = 1
    end
    if (jsonType == "control" and streams["screen_display"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["screen_display"] = streams["screen_display"]
    end
    if (jsonType == "control" and streams["wait_clean"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["wait_clean"] = streams["wait_clean"]
    end
    if (jsonType == "control" and streams["self_clean_time"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["self_clean_time"] = streams["self_clean_time"]
    end
    if (jsonType == "control" and streams["dry_clean_time"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["dry_clean_time"] = streams["dry_clean_time"]
    end
    if (jsonType == "control" and streams["ptc_load"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["ptc_load"] = streams["ptc_load"]
    end
    if (jsonType == "control" and streams["defrosting_load"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["defrosting_load"] = streams["defrosting_load"]
    end
    if (jsonType == "control" and streams["no_wind_sense_judge_param"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["no_wind_sense_judge_param"] = streams["no_wind_sense_judge_param"]
    end
    if (jsonType == "control" and streams["left_ud_wind_angle"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["left_ud_wind_angle"] = streams["left_ud_wind_angle"]
    end
    if (jsonType == "control" and streams["up_lr_wind_angle"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["up_lr_wind_angle"] = streams["up_lr_wind_angle"]
    end
    if (jsonType == "control" and streams["swing_lr_under_angle"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["swing_lr_under_angle"] = streams["swing_lr_under_angle"]
    end
    if (jsonType == "control" and streams["right_ud_wind_angle"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["right_ud_wind_angle"] = streams["right_ud_wind_angle"]
    end
    if (jsonType == "control" and streams["left_lr_wind_angle"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["left_lr_wind_angle"] = streams["left_lr_wind_angle"]
    end
    if (jsonType == "control" and streams["right_lr_wind_angle"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["right_lr_wind_angle"] = streams["right_lr_wind_angle"]
    end
    if (jsonType == "control" and streams["jet_cool"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        if (streams["jet_cool"] == keyV["VALUE_FUNCTION_ON"]) then keyP["jet_cool"] = 0x01 elseif (streams["jet_cool"] == keyV["VALUE_FUNCTION_OFF"]) then keyP["jet_cool"] = 0x00 end
    end
    if (jsonType == "control" and (streams["wind_swing_ud_angle_up"] ~= nil or streams["wind_swing_ud_angle_down"] ~= nil or streams["app_control_remember_ud"] ~= nil)) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["wind_swing_ud_angle_switch"] = 1
    end
    if (streams["wind_swing_ud_angle_up"] ~= nil) then keyP["wind_swing_ud_angle_up"] = streams
        ["wind_swing_ud_angle_up"] end
    if (streams["wind_swing_ud_angle_down"] ~= nil) then keyP["wind_swing_ud_angle_down"] = streams
        ["wind_swing_ud_angle_down"] end
    if (streams["app_control_remember_ud"] ~= nil) then keyP["app_control_remember_ud"] = streams
        ["app_control_remember_ud"] end
    if (jsonType == "control" and (streams["wind_swing_lr_angle_up"] ~= nil or streams["wind_swing_lr_angle_down"] ~= nil or streams["app_control_remember_lr"] ~= nil)) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["wind_swing_lr_angle_switch"] = 1
    end
    if (streams["wind_swing_lr_angle_up"] ~= nil) then keyP["wind_swing_lr_angle_up"] = streams
        ["wind_swing_lr_angle_up"] end
    if (streams["wind_swing_lr_angle_down"] ~= nil) then keyP["wind_swing_lr_angle_down"] = streams
        ["wind_swing_lr_angle_down"] end
    if (streams["app_control_remember_lr"] ~= nil) then keyP["app_control_remember_lr"] = streams
        ["app_control_remember_lr"] end
    if (jsonType == "control" and streams["smart_dry_value"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["smart_dry_value"] = streams["smart_dry_value"]
    end
    if (jsonType == "control" and (streams["no_wind_sense_up"] ~= nil or streams["no_wind_sense_down"] ~= nil)) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["no_wind_sense_updown_control"] = 1
    end
    if (streams["no_wind_sense_up"] ~= nil) then keyP["no_wind_sense_up"] = streams["no_wind_sense_up"] end
    if (streams["no_wind_sense_down"] ~= nil) then keyP["no_wind_sense_down"] = streams["no_wind_sense_down"] end
    if (jsonType == "control" and streams["screen_display_select"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["screen_display_select"] = streams["screen_display_select"]
    end
    if (jsonType == "control" and streams["auto_prevent_cold_wind"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["auto_prevent_cold_wind"] = streams["auto_prevent_cold_wind"]
    end
    if (jsonType == "control" and streams["linkage_2"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["linkage_2"] = streams["linkage_2"]
    end
    if (jsonType == "control" and streams["cool_power_saving"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["cool_power_saving"] = streams["cool_power_saving"]
    end
    if (jsonType == "control" and (streams["ieco_target_rate"] ~= nil or streams["ieco_indoor_wind_speed"] ~= nil or streams["ieco_outdoor_wind_speed"] ~= nil or streams["ieco_frame"] ~= nil or streams["ieco_expansion_valve"] ~= nil or streams["ieco_switch"] ~= nil)) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["ieco_status"] = 1
    end
    if (streams["ieco_switch"] ~= nil) then keyP["ieco_switch"] = streams["ieco_switch"] end
    if (streams["ieco_target_rate"] ~= nil) then keyP["ieco_target_rate"] = streams["ieco_target_rate"] end
    if (streams["ieco_indoor_wind_speed"] ~= nil) then keyP["ieco_indoor_wind_speed"] = streams
        ["ieco_indoor_wind_speed"] end
    if (streams["ieco_outdoor_wind_speed"] ~= nil) then keyP["ieco_outdoor_wind_speed"] = streams
        ["ieco_outdoor_wind_speed"] end
    if (streams["ieco_frame"] ~= nil) then keyP["ieco_frame"] = streams["ieco_frame"] end
    if (streams["ieco_expansion_valve"] ~= nil) then keyP["ieco_expansion_valve"] = streams["ieco_expansion_valve"] end
    if (streams["ieco_indoor_wind_speed_level"] ~= nil) then keyP["ieco_indoor_wind_speed_level"] = streams
        ["ieco_indoor_wind_speed_level"] end
    if (streams["ieco_outdoor_wind_speed_level"] ~= nil) then keyP["ieco_outdoor_wind_speed_level"] = streams
        ["ieco_outdoor_wind_speed_level"] end
    if (streams["ieco_number"] ~= nil) then keyP["ieco_number"] = streams["ieco_number"] end
    if (streams["has_ieco"] ~= nil) then keyP["has_ieco"] = streams["has_ieco"] end
    if (jsonType == "control" and streams["quick_cool_heat"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["quick_cool_heat"] = streams["quick_cool_heat"]
    end
    if (jsonType == "control" and streams["prepare_food"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["prepare_food"] = streams["prepare_food"]
    end
    if (streams["prepare_food_temp"] ~= nil) then keyP["prepare_food_temp"] = streams["prepare_food_temp"] end
    if (streams["prepare_food_fan_speed"] ~= nil) then keyP["prepare_food_fan_speed"] = streams
        ["prepare_food_fan_speed"] end
    if (jsonType == "control" and streams["quick_fry"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["quick_fry"] = streams["quick_fry"]
    end
    if (streams["quick_fry_temp"] ~= nil) then keyP["quick_fry_temp"] = streams["quick_fry_temp"] end
    if (streams["quick_fry_fan_speed"] ~= nil) then keyP["quick_fry_fan_speed"] = streams["quick_fry_fan_speed"] end
    if (jsonType == "control" and (streams["quick_fry_center_point"] ~= nil or streams["quick_fry_angle"] ~= nil)) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["quick_fry_control"] = 1
    end
    if (streams["quick_fry_center_point"] ~= nil) then keyP["quick_fry_center_point"] = streams
        ["quick_fry_center_point"] end
    if (streams["quick_fry_angle"] ~= nil) then keyP["quick_fry_angle"] = streams["quick_fry_angle"] end
    if (jsonType == "control" and streams["care_mode"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["care_mode"] = streams["care_mode"]
    end
    if (jsonType == "control" and streams["care_mode_lock"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["care_mode_lock"] = streams["care_mode_lock"]
    end
    if (streams["cool_light_color_r"] ~= nil) then keyP["cool_light_color_r"] = streams["cool_light_color_r"] end
    if (streams["cool_light_color_g"] ~= nil) then keyP["cool_light_color_g"] = streams["cool_light_color_g"] end
    if (streams["cool_light_color_b"] ~= nil) then keyP["cool_light_color_b"] = streams["cool_light_color_b"] end
    if (streams["heat_light_color_r"] ~= nil) then keyP["heat_light_color_r"] = streams["heat_light_color_r"] end
    if (streams["heat_light_color_g"] ~= nil) then keyP["heat_light_color_g"] = streams["heat_light_color_g"] end
    if (streams["heat_light_color_b"] ~= nil) then keyP["heat_light_color_b"] = streams["heat_light_color_b"] end
    if (streams["dry_light_color_r"] ~= nil) then keyP["dry_light_color_r"] = streams["dry_light_color_r"] end
    if (streams["dry_light_color_g"] ~= nil) then keyP["dry_light_color_g"] = streams["dry_light_color_g"] end
    if (streams["dry_light_color_b"] ~= nil) then keyP["dry_light_color_b"] = streams["dry_light_color_b"] end
    if (streams["remove_odor_light_color_r"] ~= nil) then keyP["remove_odor_light_color_r"] = streams
        ["remove_odor_light_color_r"] end
    if (streams["remove_odor_light_color_g"] ~= nil) then keyP["remove_odor_light_color_g"] = streams
        ["remove_odor_light_color_g"] end
    if (streams["remove_odor_light_color_b"] ~= nil) then keyP["remove_odor_light_color_b"] = streams
        ["remove_odor_light_color_b"] end
    if (streams["fresh_light_color_r"] ~= nil) then keyP["fresh_light_color_r"] = streams["fresh_light_color_r"] end
    if (streams["fresh_light_color_g"] ~= nil) then keyP["fresh_light_color_g"] = streams["fresh_light_color_g"] end
    if (streams["fresh_light_color_b"] ~= nil) then keyP["fresh_light_color_b"] = streams["fresh_light_color_b"] end
    if (streams["purifier_light_color_r"] ~= nil) then keyP["purifier_light_color_r"] = streams
        ["purifier_light_color_r"] end
    if (streams["purifier_light_color_g"] ~= nil) then keyP["purifier_light_color_g"] = streams
        ["purifier_light_color_g"] end
    if (streams["purifier_light_color_b"] ~= nil) then keyP["purifier_light_color_b"] = streams
        ["purifier_light_color_b"] end
    if (jsonType == "control" and (streams["cool_light_color_r"] ~= nil or streams["cool_light_color_g"] ~= nil or streams["cool_light_color_b"] ~= nil or streams["heat_light_color_r"] ~= nil or streams["heat_light_color_g"] ~= nil or streams["heat_light_color_b"] ~= nil or streams["dry_light_color_r"] ~= nil or streams["dry_light_color_g"] ~= nil or streams["dry_light_color_b"] ~= nil or streams["remove_odor_light_color_r"] ~= nil or streams["remove_odor_light_color_g"] ~= nil or streams["remove_odor_light_color_b"] ~= nil or streams["fresh_light_color_r"] ~= nil or streams["fresh_light_color_g"] ~= nil or streams["fresh_light_color_b"] ~= nil or streams["purifier_light_color_r"] ~= nil or streams["purifier_light_color_g"] ~= nil or streams["purifier_light_color_b"] ~= nil)) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["light_color_control"] = 1
    end
    if (streams["breath_cool"] ~= nil) then keyP["breath_cool"] = streams["breath_cool"] end
    if (streams["breath_heat"] ~= nil) then keyP["breath_heat"] = streams["breath_heat"] end
    if (streams["breath_remove_odor"] ~= nil) then keyP["breath_remove_odor"] = streams["breath_remove_odor"] end
    if (streams["breath_fresh_air"] ~= nil) then keyP["breath_fresh_air"] = streams["breath_fresh_air"] end
    if (streams["breath_purifier"] ~= nil) then keyP["breath_purifier"] = streams["breath_purifier"] end
    if (jsonType == "control" and streams["dust_full_time_reset"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["dust_full_time_reset"] = streams["dust_full_time_reset"]
    end
    if (jsonType == "control" and streams["circle_fan"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["circle_fan"] = streams["circle_fan"]
    end
    if (streams["circle_fan_mode"] ~= nil) then keyP["circle_fan_mode"] = streams["circle_fan_mode"] end
    if (jsonType == "control" and streams["linkage_2_temp_control_type"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["linkage_2_temp_control_type"] = streams["linkage_2_temp_control_type"]
    end
    if (streams["linkage_2_fresh_air_control_type"] ~= nil) then keyP["linkage_2_fresh_air_control_type"] = streams
        ["linkage_2_fresh_air_control_type"] end
    if (streams["linkage_2_humi_control_type"] ~= nil) then keyP["linkage_2_humi_control_type"] = streams
        ["linkage_2_humi_control_type"] end
    if (streams["linkage_2_purifier_control_type"] ~= nil) then keyP["linkage_2_purifier_control_type"] = streams
        ["linkage_2_purifier_control_type"] end
    if (streams["linkage_2_wind_control_type"] ~= nil) then keyP["linkage_2_wind_control_type"] = streams
        ["linkage_2_wind_control_type"] end
    if (jsonType == "control" and streams["prevent_straight_wind_distance"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["prevent_straight_wind_distance"] = streams["prevent_straight_wind_distance"]
    end
    if (jsonType == "control" and streams["auto_prevent_cold_wind_memory"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["auto_prevent_cold_wind_memory"] = streams["auto_prevent_cold_wind_memory"]
    end
    if (jsonType == "control" and streams["buzzer_off_status"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["buzzer_off_status"] = streams["buzzer_off_status"]
    end
    if (jsonType == "control" and streams["air_remove_odor"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["air_remove_odor"] = streams["air_remove_odor"]
    end
    if (jsonType == "control" and (streams["eco_time_switch"] ~= nil or streams["eco_time_sec"] ~= nil or streams["eco_time_min"] ~= nil or streams["eco_time_hour"] ~= nil)) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["eco_time_status"] = 1
    end
    if (streams["eco_time_switch"] ~= nil) then keyP["eco_time_switch"] = streams["eco_time_switch"] end
    if (streams["eco_time_sec"] ~= nil) then keyP["eco_time_sec"] = streams["eco_time_sec"] end
    if (streams["eco_time_min"] ~= nil) then keyP["eco_time_min"] = streams["eco_time_min"] end
    if (streams["eco_time_hour"] ~= nil) then keyP["eco_time_hour"] = streams["eco_time_hour"] end
    if (streams["dynamic_temp_compensation"] ~= nil) then keyP["dynamic_temp_compensation"] = streams
        ["dynamic_temp_compensation"] end
    if (streams["frequency_compensation"] ~= nil) then keyP["frequency_compensation"] = streams
        ["frequency_compensation"] end
    if (jsonType == "control" and streams["clean_breath"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["clean_breath"] = streams["clean_breath"]
    end
    if (streams["clean_breath_level"] ~= nil) then keyP["clean_breath_level"] = streams["clean_breath_level"] end
    if (jsonType == "control" and streams["health"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["health"] = streams["health"]
    end
    if (jsonType == "control" and streams["remove_arofene_clean"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["remove_arofene_clean"] = streams["remove_arofene_clean"]
    end
    if (jsonType == "control" and streams["control_source"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["control_source"] = streams["control_source"]
    end
    if (jsonType == "control" and streams["humidification"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["humidification"] = streams["humidification"]
    end
    if (streams["humidification_fan_speed"] ~= nil) then keyP["humidification_fan_speed"] = streams
        ["humidification_fan_speed"] end
    if (streams["humidification_mode"] ~= nil) then keyP["humidification_mode"] = streams["humidification_mode"] end
    if (jsonType == "control" and streams["strong_cool"] ~= nil) then
        keyP["propertyNumber"] = keyP["propertyNumber"] + 1
        keyP["strong_cool"] = streams["strong_cool"]
    end
    if (jsonType == "status") then keyP["propertyNumber"] = 0 end
end
local function binToModel(binData, deviceSN8)
    local messageBytes = binData
    keyP["analysis_value"] = nil
    if ((dataType == 0x02 and messageBytes[0] == 0xC0) or (dataType == 0x03 and messageBytes[0] == 0xC0) or (dataType == 0x05 and messageBytes[0] == 0xA0)) then
        if ((function(t)
                local c = 0; for _ in pairs(t) do c = c + 1 end
                return c
            end)(binData) < 21) then return nil end
        keyP["analysis_value"] =
        "power,mode,temperature,wind_speed,power_on_timer,smart_dry_value,power_off_timer,power_off_time_value,power_on_time_value,ptc,eco,dry,wind_swing_lr,wind_swing_lr_under,wind_swing_ud,kick_quilt,prevent_cold,small_temperature,purifier,dust_full_time,power_saving,fault_tag,wind_swing_ud_left,wind_swing_ud_right,wind_swing_lr_right,wind_swing_lr_left,inner_purifier,screen_display_now,screen_display"
        keyP["powerValue"] = bit.band(messageBytes[1], 0x01)
        keyP["modeValue"] = bit.band(messageBytes[2], 0xE0)
        if (keyP["modeValue"] == 0x20) then keyP["modeValue"] = 1 elseif (keyP["modeValue"] == 0x40) then keyP["modeValue"] = 2 elseif (keyP["modeValue"] == 0x60) then keyP["modeValue"] = 3 elseif (keyP["modeValue"] == 0x80) then keyP["modeValue"] = 4 elseif (keyP["modeValue"] == 0xA0) then keyP["modeValue"] = 5 elseif (keyP["modeValue"] == 0xC0) then keyP["modeValue"] = 6 end
        keyP["fault_tag"] = bit.rshift(bit.band(messageBytes[1], 0x80), 7)
        if (keyP["modeValue"] == keyB["BYTE_MODE_SMART_DRY"]) then if (dataType == 0x05) then keyP["smartDryValue"] = bit
                .band(messageBytes[13], 0x7F) else keyP["smartDryValue"] = bit.band(messageBytes[19], 0x7F) end end
        if (dataType == 0x05 and messageBytes[0] == 0xA0) then keyP["is_query"] = 0 end
        if (dataType == 0x05) then if deviceSN8 == "11447" or deviceSN8 == "11451" or deviceSN8 == "11453" or deviceSN8 == "11455" or deviceSN8 == "11457" or deviceSN8 == "11459" or deviceSN8 == "11525" or deviceSN8 == "11527" or deviceSN8 == "11533" or deviceSN8 == "11535" then
                keyP["temperature"] = bit.rshift(bit.band(messageBytes[1], 0x7C), 2) + 0x0C
                keyP["smallTemperature"] = bit.rshift(bit.band(messageBytes[1], 0x02), 1)
            else
                keyP["temperature"] = bit.rshift(bit.band(messageBytes[1], 0x3E), 1) + 0x0C
                keyP["smallTemperature"] = bit.rshift(bit.band(messageBytes[1], 0x40), 6)
            end else
            keyP["temperature"] = bit.band(messageBytes[2], 0x0F) + 0x10
            keyP["smallTemperature"] = bit.rshift(bit.band(messageBytes[2], 0x10), 4)
        end
        keyP["fanspeedValue"] = bit.band(messageBytes[3], 0x7F)
        if (bit.band(messageBytes[4], keyB["BYTE_START_TIMER_SWITCH_ON"]) == keyB["BYTE_START_TIMER_SWITCH_ON"]) then keyP["openTimerSwitch"] =
            keyB["BYTE_START_TIMER_SWITCH_ON"] else keyP["openTimerSwitch"] = keyB["BYTE_START_TIMER_SWITCH_OFF"] end
        if (bit.band(messageBytes[5], keyB["BYTE_CLOSE_TIMER_SWITCH_ON"]) == keyB["BYTE_CLOSE_TIMER_SWITCH_ON"]) then keyP["closeTimerSwitch"] =
            keyB["BYTE_CLOSE_TIMER_SWITCH_ON"] else keyP["closeTimerSwitch"] = keyB["BYTE_CLOSE_TIMER_SWITCH_OFF"] end
        keyP["closeHour"] = bit.rshift(bit.band(messageBytes[5], 0x7F), 2)
        keyP["closeStepMintues"] = bit.band(messageBytes[5], 0x03)
        keyP["closeMin"] = 15 - bit.band(messageBytes[6], 0x0f)
        keyP["closeTime"] = keyP["closeHour"] * 60 + keyP["closeStepMintues"] * 15 + keyP["closeMin"]
        keyP["openHour"] = bit.rshift(bit.band(messageBytes[4], 0x7F), 2)
        keyP["openStepMintues"] = bit.band(messageBytes[4], 0x03)
        keyP["openMin"] = 15 - bit.rshift(bit.band(messageBytes[6], 0xf0), 4)
        keyP["openTime"] = keyP["openHour"] * 60 + keyP["openStepMintues"] * 15 + keyP["openMin"]
        keyP["strongWindValue"] = bit.band(messageBytes[8], 0x20)
        keyP["power_saving"] = bit.band(messageBytes[8], 0x08)
        keyP["comfortableSleepValue"] = bit.band(messageBytes[8], 0x03)
        keyP["comfortableSleepSwitch"] = bit.band(messageBytes[9], 0x40)
        if (dataType == 0x05) then
            keyP["comfortableSleepSwitch"] = bit.band(messageBytes[14], 0x01)
            keyP["naturalWind"] = bit.band(messageBytes[10], 0x40)
            keyP["screenDisplayNowValue"] = bit.band(messageBytes[11], 0x07)
            keyP["pmv"] = bit.rshift(bit.band(messageBytes[11], 0xF0), 4) * 0.5 - 3.5
            keyP["swingLRValueUnder"] = bit.band(messageBytes[9], 0x40)
        else
            keyP["comfortableSleepSwitch"] = bit.band(messageBytes[9], 0x40)
            keyP["naturalWind"] = bit.band(messageBytes[9], 0x02)
            keyP["screenDisplayNowValue"] = bit.rshift(bit.band(messageBytes[14], 0x70), 4)
            keyP["pmv"] = bit.band(messageBytes[14], 0x0f) * 0.5 - 3.5
            keyP["swingLRValueUnder"] = bit.band(messageBytes[20], 0x80)
        end
        keyP["PTCValue"] = bit.band(messageBytes[9], 0x08)
        keyP["purifierValue"] = bit.band(messageBytes[9], 0x20)
        keyP["inner_purifier"] = bit.rshift(bit.band(messageBytes[9], 0x20), 5)
        keyP["ecoValue"] = bit.lshift(bit.band(messageBytes[9], 0x10), 3)
        keyP["dryValue"] = bit.band(messageBytes[9], 0x04)
        if (keyP["dryValue"] == 0x04) then keyP["dryValue"] = 1 end
        keyP["swingLRValue"] = bit.band(messageBytes[7], 0x03)
        if (keyP["swingLRValue"] == 0x03) then keyP["swingLRValue"] = 1 end
        keyP["wind_swing_lr_right"] = bit.band(messageBytes[7], 0x01)
        keyP["wind_swing_lr_left"] = bit.band(messageBytes[7], 0x02)
        if (keyP["wind_swing_lr_left"] == 0x02) then keyP["wind_swing_lr_left"] = 1 end
        keyP["swingUDValue"] = bit.band(messageBytes[7], 0x0C)
        if (keyP["swingUDValue"] == 0x0C) then keyP["swingUDValue"] = 1 end
        keyP["wind_swing_ud_right"] = bit.band(messageBytes[7], 0x04)
        if (keyP["wind_swing_ud_right"] == 0x04) then keyP["wind_swing_ud_right"] = 1 end
        keyP["wind_swing_ud_left"] = bit.band(messageBytes[7], 0x08)
        if (keyP["wind_swing_ud_left"] == 0x08) then keyP["wind_swing_ud_left"] = 1 end
        keyP["swingLRUnderSwitch"] = bit.band(messageBytes[19], 0x80)
        if (dataType == 0x02 or dataType == 0x03) then
            if ((messageBytes[11] ~= 0) and (messageBytes[11] ~= 0xFF)) then
                keyP["indoorTemperatureValue"] = (messageBytes[11] - 50) / 2
                keyP["smallIndoorTemperatureValue"] = bit.band(messageBytes[15], 0xF); keyP["analysis_value"] = keyP
                ["analysis_value"] .. ",indoor_temperature"
            end
            if ((messageBytes[12] ~= 0) and (messageBytes[12] ~= 0xFF)) then
                keyP["outdoorTemperatureValue"]      = (messageBytes[12] - 50) / 2
                keyP["smallOutdoorTemperatureValue"] = bit.rshift(messageBytes[15], 4); keyP["analysis_value"] = keyP
                ["analysis_value"] .. ",outdoor_temperature"
            end
        end
        keyP["errorCode"] = messageBytes[16]
        if (dataType == 0x02 or dataType == 0x03) then keyP["dust_full_time"] = bit.rshift(
            bit.band(messageBytes[13], 0x20), 5) end
        keyP["kickQuilt"] = bit.rshift(bit.band(messageBytes[10], 0x04), 2)
        if (dataType == 0x05) then keyP["preventCold"] = bit.rshift(bit.band(messageBytes[10], 0x08), 3) else keyP["preventCold"] =
            bit.rshift(bit.band(messageBytes[10], 0x20), 5) end
        if (dataType == 0x05) then
            local temp = bit.rshift(bit.band(messageBytes[12], 0x3E), 1)
            if (temp > 0 and temp <= 25) then keyP["temperature"] = temp + 12 end
        else
            local temp = bit.band(messageBytes[13], 0x1F)
            if (temp > 0 and temp <= 25) then keyP["temperature"] = temp + 12 end
        end
        if (dataType == 0x05) then
            keyP["arom_old"] = bit.rshift(bit.band(messageBytes[21], 0x80), 7)
            keyP["analysis_value"] = keyP["analysis_value"] .. ",arom_old"
        end
        if (messageBytes[0] == 0xA0) then
            keyP["comfortPowerSave"] = bit.band(messageBytes[14], 0x01)
            keyP["analysis_value"] = keyP["analysis_value"] .. ",comfort_power_save"
        else if (#binData >= 24) then
                keyP["comfortPowerSave"] = bit.band(messageBytes[22], 0x01)
                keyP["analysis_value"] = keyP["analysis_value"] .. ",comfort_power_save"
            end end
        if (dataType == 0x05) then keyP["rewarming_dry"] = bit.rshift(bit.band(messageBytes[23], 0x02), 1) end
        if (dataType == 0x05) then if (#binData >= 24) then
                keyP["wind_speed_right"] = bit.band(messageBytes[24], 0x7F)
                keyP["analysis_value"] = keyP["analysis_value"] .. ",wind_speed_right"
            end else if (#binData >= 30) then keyP["wind_speed_right"] = bit.band(messageBytes[30], 0x7F) end end
        if (dataType == 0x05) then if (#binData >= 26) then
                keyP["indoor_co2"] = bit.bor(bit.lshift(messageBytes[26], 8), messageBytes[25])
                keyP["whirl_wind_right"] = bit.rshift(bit.band(messageBytes[27], 0x08), 3)
                keyP["whirl_wind_left"] = bit.rshift(bit.band(messageBytes[27], 0x04), 2)
            end end
        if (#binData >= 29) then
            keyP["fresh_filter_time_total"] = messageBytes[25] * 256 + messageBytes[24]
            keyP["fresh_filter_time_use"] = messageBytes[27] * 256 + messageBytes[26]
            keyP["analysis_value"] = keyP["analysis_value"] ..
            ",fresh_filter_time_total,fresh_filter_time_use,fresh_filter_timeout"
        end
        if (dataType == 0x05) then
            keyP["fresh_filter_time_use"] = messageBytes[16] * 256 + messageBytes[15]
            keyP["analysis_value"] = keyP["analysis_value"] .. ",fresh_filter_time_use"
        end
        if (dataType == 0x05) then
            keyP["analysis_value"] = keyP["analysis_value"] ..
            ",wind_swing_lr_angle,wind_swing_ud_angle,gentle_wind_sense,prevent_straight_wind,no_wind_sense,fresh_air,linkage_sync,linkage,moisturizing,no_wind_sense_right,no_wind_sense_left,ptc_default_rule,light_sensitive,self_clean,prevent_super_cool"
            keyP["light_sensitive"] = bit.rshift(bit.band(messageBytes[23], 0xC0), 6)
            keyP["ptc_default_rule"] = bit.rshift(bit.band(messageBytes[23], 0x20), 5)
            keyP["no_wind_sense_left"] = bit.band(messageBytes[27], 0x01) + 1
            keyP["no_wind_sense_right"] = bit.rshift(bit.band(messageBytes[27], 0x02), 1) + 1
            keyP["moisturizing"] = bit.rshift(bit.band(messageBytes[27], 0x80), 7)
            keyP["linkage"] = bit.rshift(bit.band(messageBytes[27], 0x20), 5)
            keyP["linkage_sync"] = bit.rshift(bit.band(messageBytes[27], 0x40), 6)
            keyP["self_clean"] = bit.rshift(bit.band(messageBytes[8], 0x04), 2)
            keyP["prevent_super_cool"] = bit.rshift(bit.band(messageBytes[18], 0x40), 6)
            keyP["fresh_air"] = bit.rshift(bit.band(messageBytes[18], 0x80), 7)
            keyP["no_wind_sense"] = bit.rshift(bit.band(messageBytes[14], 0x08), 3)
            keyP["prevent_straight_wind"] = bit.rshift(bit.band(messageBytes[14], 0x40), 6)
            keyP["degerming"] = bit.rshift(bit.band(messageBytes[19], 0x02), 1)
            if (keyP["prevent_straight_wind"] == 1) then keyP["prevent_straight_wind"] = 2 end
            if (keyP["prevent_straight_wind"] == 0) then keyP["prevent_straight_wind"] = 1 end
            keyP["gentle_wind_sense"] = bit.band(messageBytes[18], 0x01)
            keyP["wind_swing_ud_angle"] = bit.band(messageBytes[17], 0x0F)
            if (keyP["wind_swing_ud_angle"] == 2) then keyP["wind_swing_ud_angle"] = 13 elseif (keyP["wind_swing_ud_angle"] == 3) then keyP["wind_swing_ud_angle"] = 25 elseif (keyP["wind_swing_ud_angle"] == 4) then keyP["wind_swing_ud_angle"] = 38 elseif (keyP["wind_swing_ud_angle"] == 5) then keyP["wind_swing_ud_angle"] = 50 elseif (keyP["wind_swing_ud_angle"] == 6) then keyP["wind_swing_ud_angle"] = 62 elseif (keyP["wind_swing_ud_angle"] == 7) then keyP["wind_swing_ud_angle"] = 75 elseif (keyP["wind_swing_ud_angle"] == 8) then keyP["wind_swing_ud_angle"] = 88 elseif (keyP["wind_swing_ud_angle"] == 9) then keyP["wind_swing_ud_angle"] = 100 end
            keyP["wind_swing_lr_angle"] = bit.rshift(bit.band(messageBytes[17], 0xF0), 4)
            if (keyP["wind_swing_lr_angle"] == 2) then keyP["wind_swing_lr_angle"] = 13 elseif (keyP["wind_swing_lr_angle"] == 3) then keyP["wind_swing_lr_angle"] = 25 elseif (keyP["wind_swing_lr_angle"] == 4) then keyP["wind_swing_lr_angle"] = 38 elseif (keyP["wind_swing_lr_angle"] == 5) then keyP["wind_swing_lr_angle"] = 50 elseif (keyP["wind_swing_lr_angle"] == 6) then keyP["wind_swing_lr_angle"] = 62 elseif (keyP["wind_swing_lr_angle"] == 7) then keyP["wind_swing_lr_angle"] = 75 elseif (keyP["wind_swing_lr_angle"] == 8) then keyP["wind_swing_lr_angle"] = 88 elseif (keyP["wind_swing_lr_angle"] == 9) then keyP["wind_swing_lr_angle"] = 100 end
            if (#binData >= 33) then
                keyP["fresh_air_mode_two"] = bit.band(messageBytes[33], 0x0F)
                keyP["fresh_air_mode"] = bit.rshift(bit.band(messageBytes[33], 0x30), 4)
                if (keyP["fresh_air_mode"] == 1) then keyP["fresh_air_mode"] = 0 elseif (keyP["fresh_air_mode"] == 3) then keyP["fresh_air_mode"] = 1 end
                keyP["inner_purifier_mode"] = bit.rshift(bit.band(messageBytes[33], 0x40), 6)
                keyP["moisturizing_fan_speed"] = messageBytes[32]
                keyP["fresh_air_fan_speed"] = messageBytes[34]
                keyP["inner_purifier_fan_speed"] = messageBytes[35]
                -- keyP["indoor_humidity"] = messageBytes[36]  -- always 0, use C1/0x45 instead
                keyP["five_dimension_mode"] = bit.band(messageBytes[37], 0x03)
                keyP["total_status_switch"] = bit.rshift(bit.band(messageBytes[37], 0x04), 2)
                keyP["wind_no_linkage"] = bit.rshift(bit.band(messageBytes[37], 0x10), 4)
                keyP["jet_cool"] = bit.rshift(bit.band(messageBytes[37], 0x08), 3)
                keyP["quick_fry"] = bit.rshift(bit.band(messageBytes[37], 0x20), 5)
                keyP["prepare_food"] = bit.rshift(bit.band(messageBytes[37], 0x40), 6)
                keyP["analysis_value"] = keyP["analysis_value"] ..
                ",fresh_air_mode,fresh_air_mode_two,inner_purifier_mode,moisturizing_fan_speed,fresh_air_fan_speed,inner_purifier_fan_speed,indoor_humidity,five_dimension_mode,total_status_switch,wind_no_linkage,jet_cool,quick_fry,prepare_food"
            end
            if (#binData >= 38) then
                keyP["screen_display_time"] = messageBytes[39]
                keyP["linkage_fan_speed"] = bit.band(messageBytes[38], 0x7F)
                if ((messageBytes[40] ~= 0xFF)) then
                    keyP["indoorTemperatureValue"] = (messageBytes[40] - 50) / 2
                    keyP["smallIndoorTemperatureValue"] = bit.band(messageBytes[41], 0x0F)
                end
                keyP["wait_clean"] = bit.rshift(bit.band(messageBytes[41], 0x40), 6)
                keyP["no_wind_sense_judge_param"] = bit.rshift(bit.band(messageBytes[41], 0x80), 7)
                keyP["analysis_value"] = keyP["analysis_value"] ..
                ",screen_display_time,linkage_fan_speed,indoor_temperature,wait_clean,no_wind_sense_judge_param"
            end
        end
    end
    if ((dataType == 0x04 and messageBytes[0] == 0xA1)) then
        keyP["is_query"] = 0
        keyP["currentWorkTime"] = bit.bor((bit.band(bit.lshift(messageBytes[9], 8), 0xFF00)),
            (bit.band(messageBytes[10], 0x00FF))) * 60 * 24 + messageBytes[11] * 60 + messageBytes[12]
        keyP["analysis_value"] = "current_work_time"
        if (messageBytes[13] ~= 0x00 and messageBytes[13] ~= 0xff) then
            keyP["indoorTemperatureValue"] = (messageBytes[13] - 50) / 2
            keyP["smallIndoorTemperatureValue"] = bit.band(messageBytes[18], 0xF); keyP["analysis_value"] = keyP
            ["analysis_value"] .. ",indoor_temperature"
        end
        if (messageBytes[14] ~= 0x00 and messageBytes[14] ~= 0xff) then
            keyP["outdoorTemperatureValue"]      = (messageBytes[14] - 50) / 2
            keyP["smallOutdoorTemperatureValue"] = bit.rshift(messageBytes[18], 4); keyP["analysis_value"] = keyP
            ["analysis_value"] .. ",outdoor_temperature"
        end
        if (#binData >= 30) then
            keyP["ptc_load"] = bit.band(messageBytes[30], 0x01)
            keyP["defrosting_load"] = bit.rshift(bit.band(messageBytes[30], 0x02), 1)
            keyP["analysis_value"] = keyP["analysis_value"] .. ",defrosting_load,ptc_load"
        end
    end
    if (messageBytes[0] == 0xC1) then
        if (messageBytes[3] == 0x40) then
            keyP["analysis_value"] =
            "electrify_time_day,electrify_time_day,electrify_time_hour,electrify_time_min,electrify_time_second,total_operating_time_day,total_operating_time_hour,total_operating_time_min,total_operating_time_second,current_operating_time_day,current_operating_time_hour,current_operating_time_min,current_operating_time_second"
            keyP["electrify_time_day"] = bit.bor(messageBytes[5], bit.bor(bit.lshift(messageBytes[4], 8)))
            keyP["electrify_time_hour"] = messageBytes[6]
            keyP["electrify_time_min"] = messageBytes[7]
            keyP["electrify_time_second"] = messageBytes[8]
            keyP["total_operating_time_day"] = bit.bor(messageBytes[10], bit.bor(bit.lshift(messageBytes[9], 8)))
            keyP["total_operating_time_hour"] = messageBytes[11]
            keyP["total_operating_time_min"] = messageBytes[12]
            keyP["total_operating_time_second"] = messageBytes[13]
            keyP["current_operating_time_day"] = bit.bor(messageBytes[15], bit.bor(bit.lshift(messageBytes[14], 8)))
            keyP["current_operating_time_hour"] = messageBytes[16]
            keyP["current_operating_time_min"] = messageBytes[17]
            keyP["current_operating_time_second"] = messageBytes[18]
        end
        if (messageBytes[3] == 0x44) then
            keyP["analysis_value"] =
            "total_power_consumption,total_operating_consumption,current_operating_consumption,current_time_power"
            keyP["total_power_consumption"] = bcd2Int(messageBytes[4]) * 10000 + bcd2Int(messageBytes[5]) * 100 +
            bcd2Int(messageBytes[6]) + bcd2Int(messageBytes[7]) / 100
            keyP["total_operating_consumption"] = bcd2Int(messageBytes[8]) * 10000 + bcd2Int(messageBytes[9]) * 100 +
            bcd2Int(messageBytes[10]) + bcd2Int(messageBytes[11]) / 100
            keyP["current_operating_consumption"] = bcd2Int(messageBytes[12]) * 10000 + bcd2Int(messageBytes[13]) * 100 +
            bcd2Int(messageBytes[14]) + bcd2Int(messageBytes[15]) / 100
            keyP["current_time_power"] = bcd2Int(messageBytes[16]) + bcd2Int(messageBytes[17]) / 100 +
            bcd2Int(messageBytes[18]) / 10000
        end
        if (messageBytes[3] == 0x45) then
            keyP["analysis_value"] = "indoor_humidity"
            keyP["indoor_humidity"] = messageBytes[4]
        end
        if (messageBytes[3] == 0x41) then keyP["t2_temp"] = (messageBytes[11] - 30) / 2 end
    end
    if (dataType == 0x05 and messageBytes[0] == 0xB5) then
        if ((function(t)
                local c = 0; for _ in pairs(t) do c = c + 1 end
                return c
            end)(binData) < 7) then return nil end
        keyP["propertyNumber"] = messageBytes[1]
        keyP["analysis_value"] = ""
        local cursor = 2
        for i = 1, keyP["propertyNumber"] do
            if (messageBytes[cursor + 0] == 0x49 and messageBytes[cursor + 1] == 0x00) then
                keyP["prevent_super_cool"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "prevent_super_cool,"
                cursor = cursor + 8
            end
            if (messageBytes[cursor + 0] == 0x42 and messageBytes[cursor + 1] == 0x00) then
                keyP["prevent_straight_wind"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "prevent_straight_wind,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x26 and messageBytes[cursor + 1] == 0x02) then
                keyP["auto_prevent_straight_wind"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "auto_prevent_straight_wind,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x39 and messageBytes[cursor + 1] == 0x00) then
                keyP["self_clean"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "self_clean,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x32 and messageBytes[cursor + 1] == 0x00) then
                if (messageBytes[cursor + 3] == 0x01) then
                    keyP["wind_straight"] = 0x01
                    keyP["analysis_value"] = keyP["analysis_value"] .. "wind_straight,"
                end
                if (messageBytes[cursor + 3] == 0x02) then
                    keyP["wind_avoid"] = 0x01
                    keyP["yb_wind_avoid"] = 0x02
                    keyP["analysis_value"] = keyP["analysis_value"] .. "wind_avoid,yb_wind_avoid,"
                end
                if (messageBytes[cursor + 3] == 0x00) then
                    keyP["wind_straight"] = 0x00
                    keyP["wind_avoid"] = 0x00
                    keyP["yb_wind_avoid"] = 0x00
                    keyP["analysis_value"] = keyP["analysis_value"] .. "wind_straight,wind_avoid,yb_wind_avoid,"
                end
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x33 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_avoid"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_avoid,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x34 and messageBytes[cursor + 1] == 0x00) then
                keyP["intelligent_wind"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "intelligent_wind,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x3A and messageBytes[cursor + 1] == 0x00) then
                keyP["child_prevent_cold_wind"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "child_prevent_cold_wind,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x18 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 3] == 0x02) then
                    keyP["fn_no_wind_sense"] = messageBytes[cursor + 3]
                    keyP["no_wind_sense_level"] = messageBytes[cursor + 4]
                    keyP["analysis_value"] = keyP["analysis_value"] .. "fn_no_wind_sense,no_wind_sense_level,"
                    cursor = cursor + 5
                else
                    keyP["no_wind_sense"] = messageBytes[cursor + 3]
                    keyP["analysis_value"] = keyP["analysis_value"] .. "no_wind_sense,"
                    cursor = cursor + 4
                end end
            if (messageBytes[cursor + 0] == 0x1B and messageBytes[cursor + 1] == 0x02) then
                keyP["little_angel"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "little_angel,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x21 and messageBytes[cursor + 1] == 0x00) then
                keyP["cool_hot_sense"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "cool_hot_sense,"
                cursor = cursor + 11
            end
            if (messageBytes[cursor + 0] == 0x29 and messageBytes[cursor + 1] == 0x00) then
                keyP["security"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "security,"
                if (messageBytes[cursor + 3] == 2) then keyP["security"] = 0 end
                if (messageBytes[cursor + 3] == 3) then keyP["security"] = 1 end
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x4E and messageBytes[cursor + 1] == 0x00) then
                keyP["even_wind"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "even_wind,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x4F and messageBytes[cursor + 1] == 0x00) then
                keyP["single_tuyere"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "single_tuyere,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x4C and messageBytes[cursor + 1] == 0x00) then
                keyP["extreme_wind"] = messageBytes[cursor + 3]
                keyP["extreme_wind_level"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "extreme_wind,extreme_wind_level,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x20 and messageBytes[cursor + 1] == 0x00) then
                keyP["voice_control"] = messageBytes[cursor + 3]
                keyP["voice_control_new"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "voice_control,voice_control_new,"
                cursor = cursor + 23
            end
            if (messageBytes[cursor + 0] == 0x01 and messageBytes[cursor + 1] == 0x02) then
                keyP["pre_cool_hot"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "pre_cool_hot,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x4A and messageBytes[cursor + 1] == 0x00) then
                keyP["water_washing_manual"] = messageBytes[cursor + 3]
                keyP["water_washing"] = messageBytes[cursor + 4]
                keyP["water_washing_time"] = messageBytes[cursor + 5]
                keyP["water_washing_stage"] = messageBytes[cursor + 6]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "water_washing_manual,water_washing,water_washing_time,water_washing_stage,"
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x4B and messageBytes[cursor + 1] == 0x00) then
                keyP["fresh_air"] = messageBytes[cursor + 3]
                keyP["fresh_air_fan_speed"] = messageBytes[cursor + 4]
                keyP["fresh_air_temp"] = messageBytes[cursor + 5]
                keyP["fresh_air_mode_two"] = messageBytes[cursor + 6]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "fresh_air,fresh_air_fan_speed,fresh_air_temp,fresh_air_mode_two,fresh_air_mode,"
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x51 and messageBytes[cursor + 1] == 0x00) then
                keyP["parent_control"] = messageBytes[cursor + 3]
                keyP["parent_control_temp_up"] = messageBytes[cursor + 4]
                keyP["parent_control_temp_down"] = messageBytes[cursor + 5]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "parent_control,parent_control_temp_up,parent_control_temp_down,"
                cursor = cursor + 8
            end
            if (messageBytes[cursor + 0] == 0x43 and messageBytes[cursor + 1] == 0x00) then
                if (messageBytes[cursor + 3] == 0x01 or messageBytes[cursor + 3] == 0x00) then end
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x30 and messageBytes[cursor + 1] == 0x00) then
                keyP["nobody_energy_save"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "nobody_energy_save,"
                cursor = cursor + 9
            end
            if (messageBytes[cursor + 0] == 0x09 and messageBytes[cursor + 1] == 0x04) then
                keyP["filter_level"] = messageBytes[cursor + 4]
                keyP["filter_value"] = messageBytes[cursor + 13]
                keyP["analysis_value"] = keyP["analysis_value"] .. "filter_level,filter_value,"
                cursor = cursor + 16
            end
            if (messageBytes[cursor + 0] == 0x58 and messageBytes[cursor + 1] == 0x00) then
                keyP["prevent_straight_wind_lr"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "prevent_straight_wind_lr,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x0B and messageBytes[cursor + 1] == 0x02) then
                keyP["pm25_value"] = messageBytes[cursor + 5] * 256 + messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "pm25_value,"
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x50 and messageBytes[cursor + 1] == 0x00) then
                keyP["water_pump"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "water_pump,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x31 and messageBytes[cursor + 1] == 0x00) then
                keyP["intelligent_control"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "intelligent_control,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x24 and messageBytes[cursor + 1] == 0x00) then
                keyP["volume_control"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "volume_control,"
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x09 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_ud_angle"] = messageBytes[cursor + 3]
                keyP["left_ud_wind_angle"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_swing_ud_angle,left_ud_wind_angle,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x0A and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_lr_angle"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_swing_lr_angle,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x44 and messageBytes[cursor + 1] == 0x00) then
                keyP["face_register"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "face_register,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x5A and messageBytes[cursor + 1] == 0x00) then
                keyP["degerming"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "degerming,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x5B and messageBytes[cursor + 1] == 0x00) then
                keyP["light"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "light,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x61 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_top"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_top,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x59 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_around"] = messageBytes[cursor + 3]
                keyP["wind_around_ud"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_around,wind_around_ud,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x1A and messageBytes[cursor + 1] == 0x00) then cursor = cursor + 4 end
            if (messageBytes[cursor + 0] == 0x25 and messageBytes[cursor + 1] == 0x02) then
                keyP["cool_temp_down"] = messageBytes[cursor + 3]
                keyP["cool_temp_up"] = messageBytes[cursor + 4]
                keyP["auto_temp_down"] = messageBytes[cursor + 5]
                keyP["auto_temp_up"] = messageBytes[cursor + 6]
                keyP["heat_temp_down"] = messageBytes[cursor + 7]
                keyP["heat_temp_up"] = messageBytes[cursor + 8]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "cool_temp_down,cool_temp_up,auto_temp_down,auto_temp_up,heat_temp_down,heat_temp_up,"
                cursor = cursor + 10
            end
            if (messageBytes[cursor + 0] == 0x27 and messageBytes[cursor + 1] == 0x02) then
                keyP["power_lock"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "power_lock"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x29 and messageBytes[cursor + 1] == 0x02) then
                keyP["ptc_lock"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "ptc_lock,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x2B and messageBytes[cursor + 1] == 0x02) then
                keyP["offline_operating_time"] = bit.bor(bit.lshift(messageBytes[cursor + 4], 8),
                    messageBytes[cursor + 3])
                keyP["analysis_value"] = keyP["analysis_value"] .. "offline_operating_time,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x28 and messageBytes[cursor + 1] == 0x02) then
                keyP["operating_time"] = bit.bor(messageBytes[cursor + 3],
                    bit.bor(bit.lshift(messageBytes[cursor + 4], 8), bit.lshift(messageBytes[cursor + 5], 16)))
                keyP["analysis_value"] = keyP["analysis_value"] .. "operating_time,"
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x15 and messageBytes[cursor + 1] == 0x00) then
                -- keyP["indoor_humidity"] = messageBytes[cursor + 3]  -- use C1/0x45 instead
                keyP["analysis_value"] = keyP["analysis_value"] .. "indoor_humidity,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x5C and messageBytes[cursor + 1] == 0x00) then
                keyP["child_lock"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "child_lock,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x2C and messageBytes[cursor + 1] == 0x02) then
                keyP["buzzer_all"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "buzzer_all,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x5D and messageBytes[cursor + 1] == 0x00) then
                keyP["self_remove_odor_phase"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "self_remove_odor_phase,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x5E and messageBytes[cursor + 1] == 0x00) then
                keyP["high_temp_remove_odor_alone"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "high_temp_remove_odor_alone,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x5F and messageBytes[cursor + 1] == 0x00) then
                keyP["ozone"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "ozone,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x63 and messageBytes[cursor + 1] == 0x00) then
                keyP["soft_warm"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "soft_warm,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x50 and messageBytes[cursor + 1] == 0x02) then
                keyP["fresh_air_parm"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "fresh_air_parm,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x68 and messageBytes[cursor + 1] == 0x00) then
                keyP["rewarming_dry"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "rewarming_dry,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x69 and messageBytes[cursor + 1] == 0x00) then
                keyP["arom"] = messageBytes[cursor + 3]
                keyP["arom_fan_speed"] = messageBytes[cursor + 4]
                keyP["arom_time_clean"] = messageBytes[cursor + 5]
                keyP["arom_time"] = bit.bor(bit.lshift(messageBytes[cursor + 7], 8), messageBytes[cursor + 6])
                keyP["arom_time_total"] = bit.bor(bit.lshift(messageBytes[cursor + 9], 8), messageBytes[cursor + 8])
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "arom,arom_fan_speed,arom_time_clean,arom_time,arom_time_total,"
                cursor = cursor + 10
            end
            if (messageBytes[cursor + 0] == 0x30 and messageBytes[cursor + 1] == 0x02) then
                keyP["main_horizontal_guide_strip_1"] = messageBytes[cursor + 3]
                keyP["main_horizontal_guide_strip_2"] = messageBytes[cursor + 4]
                keyP["main_horizontal_guide_strip_3"] = messageBytes[cursor + 5]
                keyP["main_horizontal_guide_strip_4"] = messageBytes[cursor + 6]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "main_horizontal_guide_strip_1,main_horizontal_guide_strip_2,main_horizontal_guide_strip_3,main_horizontal_guide_strip_4,"
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x6F and messageBytes[cursor + 1] == 0x00) then
                keyP["uvc_remove_odor"] = messageBytes[cursor + 3]
                keyP["uvc_power_off"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "uvc_remove_odor,uvc_power_off,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x08 and messageBytes[cursor + 1] == 0x02) then
                keyP["light_sensitive"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "light_sensitive,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x71 and messageBytes[cursor + 1] == 0x00) then
                keyP["whirl_wind_left"] = messageBytes[cursor + 3]
                keyP["whirl_wind_right"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "whirl_wind_left,whirl_wind_right,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x70 and messageBytes[cursor + 1] == 0x00) then
                keyP["inner_purifier"] = messageBytes[cursor + 3]
                keyP["inner_purifier_fan_speed"] = messageBytes[cursor + 4]
                keyP["inner_purifier_mode"] = messageBytes[cursor + 5]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "inner_purifier,inner_purifier_fan_speed,inner_purifier_mode,"
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x73 and messageBytes[cursor + 1] == 0x00) then
                keyP["indoor_co2"] = bit.bor(bit.lshift(messageBytes[cursor + 4], 8), messageBytes[cursor + 3])
                keyP["analysis_value"] = keyP["analysis_value"] .. "indoor_co2,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x77 and messageBytes[cursor + 1] == 0x00) then
                keyP["remove_odor"] = messageBytes[cursor + 3]
                keyP["remove_odor_fan_speed"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "remove_odor,remove_odor_fan_speed,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x76 and messageBytes[cursor + 1] == 0x00) then
                keyP["fresh_air_on_co2"] = bit.bor(bit.lshift(messageBytes[cursor + 4], 8), messageBytes[cursor + 3])
                keyP["fresh_air_off_co2"] = bit.bor(bit.lshift(messageBytes[cursor + 6], 8), messageBytes[cursor + 5])
                keyP["remove_odor_fan_speed"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "fresh_air_on_co2,fresh_air_off_co2,"
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x7B and messageBytes[cursor + 1] == 0x00) then
                keyP["linkage"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "linkage,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x7C and messageBytes[cursor + 1] == 0x00) then
                keyP["moisturizing"] = messageBytes[cursor + 3]
                keyP["moisturizing_fan_speed"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "moisturizing,moisturizing_fan_speed,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x74 and messageBytes[cursor + 1] == 0x00) then
                keyP["no_wind_sense_left"] = messageBytes[cursor + 3]
                keyP["no_wind_sense_right"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "no_wind_sense_left,no_wind_sense_right,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x7F and messageBytes[cursor + 1] == 0x00) then
                keyP["powerValue"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "power,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x02 and messageBytes[cursor + 1] == 0x00) then
                keyP["modeValue"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "mode,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x06 and messageBytes[cursor + 1] == 0x00) then
                keyP["fanspeedValue"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_speed,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x03 and messageBytes[cursor + 1] == 0x00) then
                keyP["temperature"] = (messageBytes[cursor + 3] - 50) / 2
                keyP["smallTemperature"] = (messageBytes[cursor + 3] - 50) % 2
                if (keyP["smallTemperature"] == 0) then keyP["smallTemperature"] = 1 end
                keyP["analysis_value"] = keyP["analysis_value"] .. "temperature,small_temperature,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x80 and messageBytes[cursor + 1] == 0x00) then
                keyP["swingLRValue"] = messageBytes[cursor + 3]
                keyP["wind_swing_lr_left"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_swing_lr,wind_swing_lr_left,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x81 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_lr_right"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_swing_lr_right,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x82 and messageBytes[cursor + 1] == 0x00) then
                keyP["swingUDValue"] = messageBytes[cursor + 3]
                keyP["wind_swing_ud_left"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_swing_ud,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x83 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_ud_right"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_swing_ud_right,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x84 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_speed_right"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_speed_right,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x10 and messageBytes[cursor + 1] == 0x00) then
                keyP["dryValue"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "dry,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x0F and messageBytes[cursor + 1] == 0x00) then
                keyP["PTCValue"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "ptc,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x11 and messageBytes[cursor + 1] == 0x02) then
                keyP["ptc_default_rule"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "ptc_default_rule,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x85 and messageBytes[cursor + 1] == 0x00) then
                keyP["fresh_filter_reset"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "fresh_filter_reset,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x17 and messageBytes[cursor + 1] == 0x00) then
                keyP["screen_display"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "screen_display,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x0D and messageBytes[cursor + 1] == 0x00) then
                keyP["ecoValue"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "ecoValue,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x0B and messageBytes[cursor + 1] == 0x00) then
                keyP["openTimerSwitch"] = messageBytes[cursor + 3]
                keyP["openHour"] = messageBytes[cursor + 4]
                keyP["openStepMintues"] = messageBytes[cursor + 5]
                keyP["analysis_value"] = keyP["analysis_value"] .. "power_on_timer,power_on_time_value"
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x0C and messageBytes[cursor + 1] == 0x00) then
                keyP["closeTimerSwitch"] = messageBytes[cursor + 3]
                keyP["closeHour"] = messageBytes[cursor + 4]
                keyP["closeStepMintues"] = messageBytes[cursor + 5]
                keyP["analysis_value"] = keyP["analysis_value"] .. "power_off_timer,power_off_time_value"
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x86 and messageBytes[cursor + 1] == 0x00) then
                keyP["gentle_wind_sense"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "gentle_wind_sense,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x22 and messageBytes[cursor + 1] == 0x00) then
                keyP["comfortPowerSave"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "comfortPowerSave,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x87 and messageBytes[cursor + 1] == 0x00) then
                keyP["screen_display_time"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "screen_display_time,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x88 and messageBytes[cursor + 1] == 0x00) then
                keyP["total_status_switch"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "total_status_switch,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x99 and messageBytes[cursor + 1] == 0x00) then
                keyP["wait_clean"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wait_clean,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x9A and messageBytes[cursor + 1] == 0x00) then
                keyP["self_clean_stage"] = messageBytes[cursor + 3]
                keyP["self_clean_time"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "self_clean_time,self_clean_stage,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x9B and messageBytes[cursor + 1] == 0x00) then
                keyP["dry_clean_stage"] = messageBytes[cursor + 3]
                keyP["dry_clean_time"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "dry_clean_time,dry_clean_stage"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x07 and messageBytes[cursor + 1] == 0x00) then
                keyP["left_down_real_wind_speed"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "left_down_real_wind_speed,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0xA4 and messageBytes[cursor + 1] == 0x00) then
                keyP["right_up_real_wind_speed"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "right_up_real_wind_speed,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0xA0 and messageBytes[cursor + 1] == 0x00) then
                keyP["ptc_load"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "ptc_load,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0xA8 and messageBytes[cursor + 1] == 0x00) then
                keyP["defrosting_load"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "defrosting_load,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x9F and messageBytes[cursor + 1] == 0x00) then
                keyP["no_wind_sense_judge_param"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "no_wind_sense_judge_param,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x0A and messageBytes[cursor + 1] == 0x00) then
                keyP["up_lr_wind_angle"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "up_lr_wind_angle,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x96 and messageBytes[cursor + 1] == 0x00) then
                keyP["swing_lr_under_angle"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "swing_lr_under_angle,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0xA1 and messageBytes[cursor + 1] == 0x00) then
                keyP["right_ud_wind_angle"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "right_ud_wind_angle,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0xA2 and messageBytes[cursor + 1] == 0x00) then
                keyP["left_lr_wind_angle"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "left_lr_wind_angle,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0xA3 and messageBytes[cursor + 1] == 0x00) then
                keyP["right_lr_wind_angle"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "right_lr_wind_angle,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x67 and messageBytes[cursor + 1] == 0x00) then
                keyP["jet_cool"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "jet_cool,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x38 and messageBytes[cursor + 1] == 0x02) then
                keyP["prevent_straight_wind_distance"] = messageBytes[cursor + 3]
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x79 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_ud_angle_up"] = messageBytes[cursor + 3]
                keyP["wind_swing_ud_angle_down"] = messageBytes[cursor + 4]
                keyP["app_control_remember_ud"] = messageBytes[cursor + 5]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "wind_swing_ud_angle_up,wind_swing_ud_angle_down,app_control_remember_ud,"
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x7A and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_lr_angle_up"] = messageBytes[cursor + 3]
                keyP["wind_swing_lr_angle_down"] = messageBytes[cursor + 4]
                keyP["app_control_remember_lr"] = messageBytes[cursor + 5]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "wind_swing_lr_angle_up,wind_swing_lr_angle_down,app_control_remember_lr,"
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0xE2 and messageBytes[cursor + 1] == 0x00) then
                keyP["left_down_real_wind_speed"] = messageBytes[cursor + 15]
                keyP["right_up_real_wind_speed"] = messageBytes[cursor + 45]
                keyP["remove_odor_time"] = messageBytes[cursor + 47]
                keyP["tvoc_level"] = messageBytes[cursor + 48]
                keyP["defrosting_load"] = bit.band(messageBytes[cursor + 16], 0x01)
                keyP["ptc_load"] = bit.rshift(bit.band(messageBytes[cursor + 16], 0x02), 1)
                keyP["self_clean_stage"] = messageBytes[cursor + 42]
                keyP["self_clean_time"] = messageBytes[cursor + 43]
                keyP["dry_clean_stage"] = bit.rshift(bit.band(messageBytes[cursor + 44], 0x80), 7)
                keyP["dry_clean_time"] = bit.band(messageBytes[cursor + 44], 0x7F)
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "defrosting_load,ptc_load,dry_clean_stage,dry_clean_time,self_clean_stage,self_clean_time,"
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xE1 and messageBytes[cursor + 1] == 0x00) then cursor = cursor +
                messageBytes[cursor + 2] + 3 end
            if (messageBytes[cursor + 0] == 0xE0 and messageBytes[cursor + 1] == 0x00) then
                keyP["tvoc_density"] = messageBytes[cursor + 25] * 256 + messageBytes[cursor + 24]
                keyP["outdoor_temperature"] = messageBytes[cursor + 13] * 256 + messageBytes[cursor + 12]
                if (keyP["outdoor_temperature"] > 32767) then keyP["outdoor_temperature"] = keyP["outdoor_temperature"] -
                    65535 - 1 end
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0x14 and messageBytes[cursor + 1] == 0x00) then
                keyP["smart_dry_value"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "smart_dry_value,"
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xAE and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_lr_under"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "wind_swing_lr_under,"
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0x36 and messageBytes[cursor + 1] == 0x02) then
                keyP["screen_display_select"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "screen_display_select,"
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xAF and messageBytes[cursor + 1] == 0x00) then
                keyP["no_wind_sense_up"] = messageBytes[cursor + 3]
                keyP["no_wind_sense_down"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "no_wind_sense_up,no_wind_sense_down,"
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0x78 and messageBytes[cursor + 1] == 0x00) then
                keyP["auto_prevent_cold_wind"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "auto_prevent_cold_wind,"
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0x89 and messageBytes[cursor + 1] == 0x00) then
                keyP["cool_power_saving"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "cool_power_saving,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x54 and messageBytes[cursor + 1] == 0x02) then
                keyP["prepare_food"] = messageBytes[cursor + 3]
                keyP["prepare_food_temp"] = messageBytes[cursor + 4]
                keyP["prepare_food_fan_speed"] = messageBytes[cursor + 5]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                "prepare_food,prepare_food_temp,prepare_food_fan_speed,"
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x55 and messageBytes[cursor + 1] == 0x02) then
                keyP["quick_fry"] = messageBytes[cursor + 3]
                keyP["quick_fry_temp"] = messageBytes[cursor + 4]
                keyP["quick_fry_fan_speed"] = messageBytes[cursor + 5]
                keyP["analysis_value"] = keyP["analysis_value"] .. "quick_fry,quick_fry_temp,quick_fry_fan_speed,"
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x8B and messageBytes[cursor + 1] == 0x00) then
                keyP["quick_fry_center_point"] = messageBytes[cursor + 3]
                keyP["quick_fry_angle"] = messageBytes[cursor + 4]
                keyP["analysis_value"] = keyP["analysis_value"] .. "quick_fry_center_point,quick_fry_angle,"
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xB5 and messageBytes[cursor + 1] == 0x00) then
                keyP["care_mode"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "care_mode,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0xB6 and messageBytes[cursor + 1] == 0x00) then
                keyP["care_mode_lock"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "care_mode_lock,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0xB8 and messageBytes[cursor + 1] == 0x00) then
                keyP["dust_full_time_reset"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "dust_full_time_reset,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0x62 and messageBytes[cursor + 1] == 0x00) then
                keyP["power_saving"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "power_saving,"
                cursor = cursor + 4
            end
            if (messageBytes[cursor + 0] == 0xB7 and messageBytes[cursor + 1] == 0x00) then
                keyP["breath_cool"] = bit.band(messageBytes[cursor + 3], 0x01)
                keyP["breath_heat"] = bit.rshift(bit.band(messageBytes[cursor + 3], 0x02), 1)
                keyP["breath_remove_odor"] = bit.rshift(bit.band(messageBytes[cursor + 3], 0x08), 3)
                keyP["breath_fresh_air"] = bit.rshift(bit.band(messageBytes[cursor + 3], 0x10), 4)
                keyP["breath_purifier"] = bit.rshift(bit.band(messageBytes[cursor + 3], 0x20), 5)
                keyP["cool_light_color_r"] = messageBytes[cursor + 4]
                keyP["cool_light_color_g"] = messageBytes[cursor + 5]
                keyP["cool_light_color_b"] = messageBytes[cursor + 6]
                keyP["heat_light_color_r"] = messageBytes[cursor + 7]
                keyP["heat_light_color_g"] = messageBytes[cursor + 8]
                keyP["heat_light_color_b"] = messageBytes[cursor + 9]
                keyP["dry_light_color_r"] = messageBytes[cursor + 10]
                keyP["dry_light_color_g"] = messageBytes[cursor + 11]
                keyP["dry_light_color_b"] = messageBytes[cursor + 12]
                keyP["remove_odor_light_color_r"] = messageBytes[cursor + 13]
                keyP["remove_odor_light_color_g"] = messageBytes[cursor + 14]
                keyP["remove_odor_light_color_b"] = messageBytes[cursor + 15]
                keyP["fresh_light_color_r"] = messageBytes[cursor + 16]
                keyP["fresh_light_color_g"] = messageBytes[cursor + 17]
                keyP["fresh_light_color_b"] = messageBytes[cursor + 18]
                keyP["purifier_light_color_r"] = messageBytes[cursor + 19]
                keyP["purifier_light_color_g"] = messageBytes[cursor + 20]
                keyP["purifier_light_color_b"] = messageBytes[cursor + 21]
                cursor = cursor + 22
            end
            if (messageBytes[cursor + 0] == 0xB2 and messageBytes[cursor + 1] == 0x00) then
                keyP["linkage_2"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "linkage_2,"
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xB3 and messageBytes[cursor + 1] == 0x00) then
                keyP["quick_cool_heat"] = messageBytes[cursor + 3]
                keyP["analysis_value"] = keyP["analysis_value"] .. "quick_cool_heat,"
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xB9 and messageBytes[cursor + 1] == 0x00) then
                keyP["circle_fan"] = messageBytes[cursor + 3]
                keyP["circle_fan_mode"] = messageBytes[cursor + 4]
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xBC and messageBytes[cursor + 1] == 0x00) then
                keyP["auto_prevent_cold_wind_memory"] = messageBytes[cursor + 3]
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0x2F and messageBytes[cursor + 1] == 0x02) then
                keyP["buzzer_off_status"] = messageBytes[cursor + 3]
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xBF and messageBytes[cursor + 1] == 0x00) then
                keyP["air_remove_odor"] = messageBytes[cursor + 3]
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xC7 and messageBytes[cursor + 1] == 0x00) then
                keyP["clean_breath"] = messageBytes[cursor + 3]
                keyP["clean_breath_level"] = messageBytes[cursor + 4]
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xC8 and messageBytes[cursor + 1] == 0x00) then
                keyP["remove_arofene_clean"] = messageBytes[cursor + 3]
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xC9 and messageBytes[cursor + 1] == 0x00) then
                keyP["health"] = messageBytes[cursor + 3]
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0xCA and messageBytes[cursor + 1] == 0x00) then
                keyP["strong_cool"] = messageBytes[cursor + 3]
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0x75 and messageBytes[cursor + 1] == 0x00) then
                keyP["humidification"] = messageBytes[cursor + 3]
                keyP["humidification_fan_speed"] = messageBytes[cursor + 4]
                keyP["humidification_mode"] = messageBytes[cursor + 5]
                cursor = cursor + messageBytes[cursor + 2] + 3
            end
            if (messageBytes[cursor + 0] == 0x7E and messageBytes[cursor + 1] == 0x00) then
                if ((function(t)
                        local c = 0; for _ in pairs(t) do c = c + 1 end
                        return c
                    end)(binData) < 21) then return nil end
                cursor = cursor - 1
                keyP["analysis_value"] =
                "power,mode,temperature,wind_speed,power_on_timer,smart_dry_value,power_off_timer,power_off_time_value,power_on_time_value,ptc,eco,dry,wind_swing_lr,wind_swing_lr_under,wind_swing_ud,kick_quilt,prevent_cold,small_temperature,purifier,dust_full_time,power_saving,fault_tag,wind_swing_ud_left,wind_swing_ud_right,wind_swing_lr_right,wind_swing_lr_left,self_clean,prevent_straight_wind,prevent_super_cool,right_ud_wind_angle,left_ud_wind_angle,left_lr_wind_angle,right_lr_wind_angle,jet_cool,wind_swing_lr_angle,wind_swing_ud_angle,degerming,ptc_default_rule,screen_display_select,swing_lr_under_angle,auto_prevent_cold_wind,no_wind_sense_up,no_wind_sense_down,screen_display_now,voice_control_new,voice_control,soft_warm"
                keyP["powerValue"] = bit.band(messageBytes[cursor + 5], 0x01)
                keyP["modeValue"] = bit.band(messageBytes[cursor + 6], 0xE0)
                if (keyP["modeValue"] == 0x20) then keyP["modeValue"] = 1 elseif (keyP["modeValue"] == 0x40) then keyP["modeValue"] = 2 elseif (keyP["modeValue"] == 0x60) then keyP["modeValue"] = 3 elseif (keyP["modeValue"] == 0x80) then keyP["modeValue"] = 4 elseif (keyP["modeValue"] == 0xA0) then keyP["modeValue"] = 5 elseif (keyP["modeValue"] == 0xC0) then keyP["modeValue"] = 6 end
                if deviceSN8 == "11447" or deviceSN8 == "11451" or deviceSN8 == "11453" or deviceSN8 == "11455" or deviceSN8 == "11457" or deviceSN8 == "11459" or deviceSN8 == "11525" or deviceSN8 == "11527" or deviceSN8 == "11533" or deviceSN8 == "11535" then
                    keyP["temperature"] = bit.rshift(bit.band(messageBytes[cursor + 5], 0x7C), 2) + 0x0C
                    keyP["smallTemperature"] = bit.rshift(bit.band(messageBytes[cursor + 5], 0x02), 1)
                else
                    keyP["temperature"] = bit.rshift(bit.band(messageBytes[cursor + 5], 0x3E), 1) + 0x0C
                    keyP["smallTemperature"] = bit.rshift(bit.band(messageBytes[cursor + 5], 0x40), 6)
                end
                keyP["fanspeedValue"] = bit.band(messageBytes[cursor + 7], 0x7F)
                if (bit.band(messageBytes[cursor + 8], keyB["BYTE_START_TIMER_SWITCH_ON"]) == keyB["BYTE_START_TIMER_SWITCH_ON"]) then keyP["openTimerSwitch"] =
                    keyB["BYTE_START_TIMER_SWITCH_ON"] else keyP["openTimerSwitch"] = keyB
                    ["BYTE_START_TIMER_SWITCH_OFF"] end
                if (bit.band(messageBytes[cursor + 9], keyB["BYTE_CLOSE_TIMER_SWITCH_ON"]) == keyB["BYTE_CLOSE_TIMER_SWITCH_ON"]) then keyP["closeTimerSwitch"] =
                    keyB["BYTE_CLOSE_TIMER_SWITCH_ON"] else keyP["closeTimerSwitch"] = keyB
                    ["BYTE_CLOSE_TIMER_SWITCH_OFF"] end
                keyP["closeHour"] = bit.rshift(bit.band(messageBytes[cursor + 9], 0x7F), 2)
                keyP["closeStepMintues"] = bit.band(messageBytes[cursor + 9], 0x03)
                keyP["closeMin"] = 15 - bit.band(messageBytes[cursor + 10], 0x0f)
                keyP["closeTime"] = keyP["closeHour"] * 60 + keyP["closeStepMintues"] * 15 + keyP["closeMin"]
                keyP["openHour"] = bit.rshift(bit.band(messageBytes[cursor + 8], 0x7F), 2)
                keyP["openStepMintues"] = bit.band(messageBytes[cursor + 8], 0x03)
                keyP["openMin"] = 15 - bit.rshift(bit.band(messageBytes[cursor + 10], 0xf0), 4)
                keyP["openTime"] = keyP["openHour"] * 60 + keyP["openStepMintues"] * 15 + keyP["openMin"]
                keyP["strongWindValue"] = bit.band(messageBytes[cursor + 12], 0x20)
                keyP["power_saving"] = bit.band(messageBytes[cursor + 12], 0x08)
                keyP["comfortableSleepValue"] = bit.band(messageBytes[cursor + 12], 0x03)
                keyP["comfortableSleepSwitch"] = bit.band(messageBytes[cursor + 12], 0x40)
                keyP["comfortableSleepSwitch"] = bit.band(messageBytes[cursor + 18], 0x01)
                keyP["naturalWind"] = bit.band(messageBytes[cursor + 14], 0x40)
                keyP["screenDisplayNowValue"] = bit.band(messageBytes[cursor + 15], 0x07)
                keyP["pmv"] = bit.rshift(bit.band(messageBytes[cursor + 15], 0xF0), 4) * 0.5 - 3.5
                keyP["swingLRValueUnder"] = bit.band(messageBytes[cursor + 13], 0x40)
                keyP["PTCValue"] = bit.band(messageBytes[cursor + 13], 0x08)
                keyP["purifierValue"] = bit.band(messageBytes[cursor + 13], 0x20)
                keyP["inner_purifier"] = bit.rshift(bit.band(messageBytes[cursor + 13], 0x20), 5)
                keyP["ecoValue"] = bit.lshift(bit.band(messageBytes[cursor + 13], 0x10), 3)
                keyP["dryValue"] = bit.band(messageBytes[cursor + 13], 0x04)
                if (keyP["dryValue"] == 0x04) then keyP["dryValue"] = 1 end
                keyP["swingLRValue"] = bit.band(messageBytes[cursor + 11], 0x03)
                if (keyP["swingLRValue"] == 0x03) then keyP["swingLRValue"] = 1 end
                keyP["wind_swing_lr_right"] = bit.band(messageBytes[cursor + 11], 0x01)
                keyP["wind_swing_lr_left"] = bit.band(messageBytes[cursor + 11], 0x02)
                if (keyP["wind_swing_lr_left"] == 0x02) then keyP["wind_swing_lr_left"] = 1 end
                keyP["swingUDValue"] = bit.band(messageBytes[cursor + 11], 0x0C)
                if (keyP["swingUDValue"] == 0x0C) then keyP["swingUDValue"] = 1 end
                keyP["wind_swing_ud_right"] = bit.band(messageBytes[cursor + 11], 0x04)
                if (keyP["wind_swing_ud_right"] == 0x04) then keyP["wind_swing_ud_right"] = 1 end
                keyP["wind_swing_ud_left"] = bit.band(messageBytes[cursor + 11], 0x08)
                if (keyP["wind_swing_ud_left"] == 0x08) then keyP["wind_swing_ud_left"] = 1 end
                keyP["swingLRUnderSwitch"] = bit.band(messageBytes[cursor + 23], 0x80)
                keyP["errorCode"] = messageBytes[cursor + 20]
                keyP["kickQuilt"] = bit.rshift(bit.band(messageBytes[cursor + 14], 0x04), 2)
                keyP["preventCold"] = bit.rshift(bit.band(messageBytes[cursor + 14], 0x08), 3)
                local temp = bit.rshift(bit.band(messageBytes[cursor + 16], 0x3E), 1)
                if (temp > 0 and temp <= 25) then keyP["temperature"] = temp + 12 end
                if (messageBytes[cursor + 4] == 0xA0) then
                    keyP["arom_old"] = bit.rshift(bit.band(messageBytes[cursor + 25], 0x80), 7)
                    keyP["analysis_value"] = keyP["analysis_value"] .. ",arom_old"
                end
                keyP["soft_warm"] = bit.rshift(bit.band(messageBytes[cursor + 24], 0x02), 1)
                keyP["wind_around"] = bit.rshift(bit.band(messageBytes[cursor + 11], 0x80), 7)
                keyP["dust_full_time"] = bit.rshift(bit.band(messageBytes[cursor + 11], 0x40), 6)
                keyP["wind_around_ud"] = bit.rshift(bit.band(messageBytes[cursor + 25], 0x18), 3)
                keyP["prevent_straight_wind_lr"] = bit.rshift(bit.band(messageBytes[cursor + 25], 0x60), 5)
                keyP["analysis_value"] = keyP["analysis_value"] .. ",wind_around,wind_around_ud,prevent_straight_wind_lr"
                keyP["comfortPowerSave"] = bit.band(messageBytes[cursor + 18], 0x01)
                keyP["analysis_value"] = keyP["analysis_value"] .. ",comfort_power_save"
                keyP["rewarming_dry"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0x02), 1)
                keyP["no_wind_sense_up"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0x04), 2)
                if (keyP["no_wind_sense_up"] == 1) then keyP["no_wind_sense_up"] = 2 else keyP["no_wind_sense_up"] = 1 end
                keyP["no_wind_sense_down"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0x08), 3)
                if (keyP["no_wind_sense_down"] == 1) then keyP["no_wind_sense_down"] = 2 else keyP["no_wind_sense_down"] = 1 end
                if (#binData >= 24) then
                    keyP["wind_speed_right"] = bit.band(messageBytes[cursor + 28], 0x7F)
                    keyP["analysis_value"] = keyP["analysis_value"] .. ",wind_speed_right"
                end
                if (#binData >= 26) then
                    keyP["indoor_co2"] = bit.bor(bit.lshift(messageBytes[cursor + 30], 8), messageBytes[cursor + 29])
                    keyP["whirl_wind_right"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x08), 3)
                    keyP["whirl_wind_left"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x04), 2)
                end
                keyP["analysis_value"] = keyP["analysis_value"] ..
                ",wind_swing_lr_angle,wind_swing_ud_angle,gentle_wind_sense,prevent_straight_wind,no_wind_sense,fresh_air,linkage_sync,linkage,moisturizing,no_wind_sense_right,no_wind_sense_left,ptc_default_rule,light_sensitive,self_clean,prevent_super_cool,cool_power_saving,quick_fry,prepare_food"
                keyP["self_clean"] = bit.rshift(bit.band(messageBytes[cursor + 12], 0x04), 2)
                keyP["prevent_super_cool"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x40), 6)
                keyP["no_wind_sense_left"] = bit.band(messageBytes[cursor + 31], 0x01) + 1
                keyP["no_wind_sense_right"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x02), 1) + 1
                keyP["moisturizing"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x80), 7)
                keyP["linkage"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x20), 5)
                keyP["linkage_sync"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x40), 6)
                keyP["smart_dry_value"] = messageBytes[cursor + 17]
                keyP["no_wind_sense"] = bit.rshift(bit.band(messageBytes[cursor + 18], 0x08), 3)
                keyP["prevent_straight_wind"] = bit.rshift(bit.band(messageBytes[cursor + 18], 0x40), 6)
                if (keyP["prevent_straight_wind"] == 1) then keyP["prevent_straight_wind"] = 2 end
                if (keyP["prevent_straight_wind"] == 0) then keyP["prevent_straight_wind"] = 1 end
                keyP["gentle_wind_sense"] = bit.band(messageBytes[cursor + 22], 0x01)
                keyP["auto_prevent_cold_wind"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x20), 5)
                keyP["wind_swing_ud_angle"] = bit.band(messageBytes[cursor + 21], 0x0F)
                keyP["degerming"] = bit.rshift(bit.band(messageBytes[cursor + 23], 0x02), 1)
                keyP["remove_odor"] = bit.rshift(bit.band(messageBytes[cursor + 23], 0x02), 1)
                if (keyP["wind_swing_ud_angle"] == 2) then keyP["wind_swing_ud_angle"] = 13 elseif (keyP["wind_swing_ud_angle"] == 3) then keyP["wind_swing_ud_angle"] = 25 elseif (keyP["wind_swing_ud_angle"] == 4) then keyP["wind_swing_ud_angle"] = 38 elseif (keyP["wind_swing_ud_angle"] == 5) then keyP["wind_swing_ud_angle"] = 50 elseif (keyP["wind_swing_ud_angle"] == 6) then keyP["wind_swing_ud_angle"] = 62 elseif (keyP["wind_swing_ud_angle"] == 7) then keyP["wind_swing_ud_angle"] = 75 elseif (keyP["wind_swing_ud_angle"] == 8) then keyP["wind_swing_ud_angle"] = 88 elseif (keyP["wind_swing_ud_angle"] == 9) then keyP["wind_swing_ud_angle"] = 100 end
                keyP["left_ud_wind_angle"] = keyP["wind_swing_ud_angle"]
                keyP["wind_swing_lr_angle"] = bit.rshift(bit.band(messageBytes[cursor + 21], 0xF0), 4)
                if (keyP["wind_swing_lr_angle"] == 2) then keyP["wind_swing_lr_angle"] = 13 elseif (keyP["wind_swing_lr_angle"] == 3) then keyP["wind_swing_lr_angle"] = 25 elseif (keyP["wind_swing_lr_angle"] == 4) then keyP["wind_swing_lr_angle"] = 38 elseif (keyP["wind_swing_lr_angle"] == 5) then keyP["wind_swing_lr_angle"] = 50 elseif (keyP["wind_swing_lr_angle"] == 6) then keyP["wind_swing_lr_angle"] = 62 elseif (keyP["wind_swing_lr_angle"] == 7) then keyP["wind_swing_lr_angle"] = 75 elseif (keyP["wind_swing_lr_angle"] == 8) then keyP["wind_swing_lr_angle"] = 88 elseif (keyP["wind_swing_lr_angle"] == 9) then keyP["wind_swing_lr_angle"] = 100 end
                keyP["left_lr_wind_angle"] = keyP["wind_swing_lr_angle"]
                if (messageBytes[cursor + 3] > 33) then
                    keyP["fresh_air_mode_two"] = bit.band(messageBytes[cursor + 37], 0x0F)
                    keyP["fresh_air_mode"] = bit.rshift(bit.band(messageBytes[cursor + 37], 0x30), 4)
                    if (keyP["fresh_air_mode"] == 1) then keyP["fresh_air_mode"] = 0 elseif (keyP["fresh_air_mode"] == 3) then keyP["fresh_air_mode"] = 1 end
                    keyP["inner_purifier_mode"] = bit.rshift(bit.band(messageBytes[cursor + 37], 0x40), 6)
                    keyP["cool_power_saving"] = bit.rshift(bit.band(messageBytes[cursor + 37], 0x80), 7)
                    keyP["moisturizing_fan_speed"] = messageBytes[cursor + 36]
                    keyP["fresh_air_fan_speed"] = messageBytes[cursor + 38]
                    keyP["inner_purifier_fan_speed"] = messageBytes[cursor + 39]
                    -- keyP["indoor_humidity"] = messageBytes[cursor + 40]  -- use C1/0x45 instead
                    keyP["five_dimension_mode"] = bit.band(messageBytes[cursor + 41], 0x03)
                    keyP["total_status_switch"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x04), 2)
                    keyP["wind_no_linkage"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x10), 4)
                    keyP["jet_cool"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x08), 3)
                    keyP["quick_fry"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x20), 5)
                    keyP["prepare_food"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x40), 6)
                end
                if (messageBytes[cursor + 3] > 38) then
                    keyP["screen_display_time"] = messageBytes[cursor + 43]
                    keyP["strong_cool"] = bit.rshift(bit.band(messageBytes[cursor + 42], 0x80), 7)
                    keyP["linkage_fan_speed"] = bit.band(messageBytes[cursor + 42], 0x7F)
                    keyP["indoorTemperatureValue"] = (messageBytes[cursor + 44] - 50) / 2
                    keyP["smallIndoorTemperatureValue"] = bit.band(messageBytes[cursor + 45], 0x0F)
                    keyP["ieco_switch"] = bit.rshift(bit.band(messageBytes[cursor + 45], 0x10), 4)
                    keyP["analysis_value"] = keyP["analysis_value"] ..
                    ",screen_display_time,linkage_fan_speed,indoor_temperature,ieco_switch"
                end
                if (messageBytes[cursor + 3] > 41) then
                    keyP["no_wind_sense_judge_param"] = bit.rshift(bit.band(messageBytes[cursor + 45], 0x80), 7)
                    keyP["wait_clean"] = bit.rshift(bit.band(messageBytes[cursor + 45], 0x40), 6)
                end
                if (messageBytes[cursor + 3] > 42) then keyP["quick_fry_center_point"] = messageBytes[cursor + 46] end
                if (messageBytes[cursor + 3] > 43) then
                    keyP["right_ud_wind_angle"] = bit.band(messageBytes[cursor + 47], 0x0F)
                    if (keyP["right_ud_wind_angle"] == 2) then keyP["right_ud_wind_angle"] = 13 elseif (keyP["right_ud_wind_angle"] == 3) then keyP["right_ud_wind_angle"] = 25 elseif (keyP["right_ud_wind_angle"] == 4) then keyP["right_ud_wind_angle"] = 38 elseif (keyP["right_ud_wind_angle"] == 5) then keyP["right_ud_wind_angle"] = 50 elseif (keyP["right_ud_wind_angle"] == 6) then keyP["right_ud_wind_angle"] = 62 elseif (keyP["right_ud_wind_angle"] == 7) then keyP["right_ud_wind_angle"] = 75 elseif (keyP["right_ud_wind_angle"] == 8) then keyP["right_ud_wind_angle"] = 88 elseif (keyP["right_ud_wind_angle"] == 9) then keyP["right_ud_wind_angle"] = 100 end
                    keyP["right_lr_wind_angle"] = bit.rshift(bit.band(messageBytes[cursor + 47], 0xF0), 4)
                    if (keyP["right_lr_wind_angle"] == 2) then keyP["right_lr_wind_angle"] = 13 elseif (keyP["right_lr_wind_angle"] == 3) then keyP["right_lr_wind_angle"] = 25 elseif (keyP["right_lr_wind_angle"] == 4) then keyP["right_lr_wind_angle"] = 38 elseif (keyP["right_lr_wind_angle"] == 5) then keyP["right_lr_wind_angle"] = 50 elseif (keyP["right_lr_wind_angle"] == 6) then keyP["right_lr_wind_angle"] = 62 elseif (keyP["right_lr_wind_angle"] == 7) then keyP["right_lr_wind_angle"] = 75 elseif (keyP["right_lr_wind_angle"] == 8) then keyP["right_lr_wind_angle"] = 88 elseif (keyP["right_lr_wind_angle"] == 9) then keyP["right_lr_wind_angle"] = 100 end
                end
                if (messageBytes[cursor + 3] > 44) then
                    keyP["screen_display_select"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x04), 2)
                    keyP["swing_lr_under_angle"] = bit.rshift(bit.band(messageBytes[cursor + 49], 0xF0), 4)
                    if (keyP["swing_lr_under_angle"] == 2) then keyP["swing_lr_under_angle"] = 13 elseif (keyP["swing_lr_under_angle"] == 3) then keyP["swing_lr_under_angle"] = 25 elseif (keyP["swing_lr_under_angle"] == 4) then keyP["swing_lr_under_angle"] = 38 elseif (keyP["swing_lr_under_angle"] == 5) then keyP["swing_lr_under_angle"] = 50 elseif (keyP["swing_lr_under_angle"] == 6) then keyP["swing_lr_under_angle"] = 62 elseif (keyP["swing_lr_under_angle"] == 7) then keyP["swing_lr_under_angle"] = 75 elseif (keyP["swing_lr_under_angle"] == 8) then keyP["swing_lr_under_angle"] = 88 elseif (keyP["swing_lr_under_angle"] == 9) then keyP["swing_lr_under_angle"] = 100 end
                end
                keyP["fresh_air"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x80), 7)
                keyP["voice_control_new"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x06), 1)
                keyP["voice_control"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x06), 1)
                keyP["ptc_default_rule"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0x20), 5)
                keyP["light_sensitive"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0xC0), 6)
                keyP["wind_swing_ud_angle_up"] = messageBytes[cursor + 32]
                keyP["wind_swing_ud_angle_down"] = messageBytes[cursor + 33]
                keyP["wind_swing_lr_angle_up"] = messageBytes[cursor + 34]
                keyP["wind_swing_lr_angle_down"] = messageBytes[cursor + 35]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                ",wind_swing_ud_angle_up,wind_swing_ud_angle_down,wind_swing_lr_angle_up,wind_swing_lr_angle_down"
                if (messageBytes[cursor + 3] > 44) then
                    keyP["app_control_remember_lr"] = bit.band(messageBytes[cursor + 48], 0x01)
                    keyP["app_control_remember_ud"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x02), 1)
                    keyP["linkage_2"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x08), 3)
                    keyP["quick_cool_heat"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x10), 4)
                    keyP["light"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x20), 5)
                    keyP["care_mode"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x40), 6)
                    keyP["care_mode_lock"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x80), 7)
                    keyP["analysis_value"] = keyP["analysis_value"] ..
                    ",app_control_remember_lr,app_control_remember_ud,linkage_2,quick_cool_heat,light"
                end
                if (messageBytes[cursor + 3] > 46) then
                    keyP["circle_fan"] = bit.rshift(bit.band(messageBytes[cursor + 50], 0x08), 3)
                    keyP["circle_fan_mode"] = bit.band(messageBytes[cursor + 50], 0x07)
                    keyP["buzzer_off_status"] = bit.rshift(bit.band(messageBytes[cursor + 50], 0x10), 4)
                    keyP["buzzer_all"] = bit.rshift(bit.band(messageBytes[cursor + 50], 0x20), 5)
                    keyP["prevent_straight_wind_distance"] = bit.rshift(bit.band(messageBytes[cursor + 50], 0xC0), 6)
                end
                if (messageBytes[cursor + 3] > 47) then
                    keyP["linkage_2_temp_auto"] = bit.band(messageBytes[cursor + 51], 0x01)
                    keyP["linkage_2_wind_auto"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x02), 1)
                    keyP["linkage_2_fresh_air_auto"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x04), 2)
                    keyP["linkage_2_purifier_auto"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x08), 3)
                    keyP["linkage_2_humi_auto"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x10), 4)
                    keyP["air_remove_odor"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x40), 6)
                    keyP["auto_prevent_cold_wind_memory"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x80), 7)
                end
                if (messageBytes[cursor + 3] > 48) then keyP["eco_time_hour"] = messageBytes[cursor + 52] end
                if (messageBytes[cursor + 3] > 50) then
                    keyP["clean_breath"] = bit.rshift(bit.band(messageBytes[cursor + 54], 0x10), 4)
                    keyP["clean_breath_level"] = bit.rshift(bit.band(messageBytes[cursor + 54], 0x0E), 1)
                    keyP["health"] = bit.rshift(bit.band(messageBytes[cursor + 54], 0x40), 6)
                    keyP["humidification_mode"] = bit.rshift(bit.band(messageBytes[cursor + 54], 0x80), 7)
                end
                if (messageBytes[cursor + 3] > 52) then keyP["arofene_filter_use_time"] = messageBytes[cursor + 56] * 256 +
                    messageBytes[cursor + 55] end
                if (messageBytes[cursor + 3] > 53) then keyP["remove_odor_fan_speed"] = messageBytes[cursor + 57] end
                if (messageBytes[cursor + 3] > 54) then
                    keyP["humidification_fan_speed"] = bit.band(messageBytes[cursor + 58], 0x7F)
                    keyP["humidification"] = bit.rshift(bit.band(messageBytes[cursor + 58], 0x80), 7)
                end
                if (#binData >= 29) then
                    keyP["fresh_filter_time_total"] = messageBytes[cursor + 29] * 256 + messageBytes[cursor + 28]
                    keyP["fresh_filter_time_use"] = messageBytes[cursor + 31] * 256 + messageBytes[cursor + 30]
                    keyP["analysis_value"] = keyP["analysis_value"] ..
                    ",fresh_filter_time_total,fresh_filter_time_use,fresh_filter_timeout"
                end
                keyP["fresh_filter_time_use"] = messageBytes[cursor + 20] * 256 + messageBytes[cursor + 19]
                keyP["analysis_value"] = keyP["analysis_value"] .. ",fresh_filter_time_use"
                cursor = cursor + messageBytes[cursor + 3] + 4
            end
        end
        if (#keyP["analysis_value"] > 1) then keyP["analysis_value"] = string.sub(keyP["analysis_value"], 1, -2) end
    end
    if ((dataType == 0x02 and messageBytes[0] == 0xB0) or (dataType == 0x03 and messageBytes[0] == 0xB1)) then
        if ((function(t)
                local c = 0; for _ in pairs(t) do c = c + 1 end
                return c
            end)(binData) < 8) then return nil end
        keyP["propertyNumber"] = messageBytes[1]
        local cursor = 2
        for i = 1, keyP["propertyNumber"] do
            if (messageBytes[cursor + 0] == 0x49 and messageBytes[cursor + 1] == 0x00) then
                keyP["prevent_super_cool"] = messageBytes[cursor + 4]
                cursor = cursor + 9
            end
            if (messageBytes[cursor + 0] == 0x42 and messageBytes[cursor + 1] == 0x00) then
                keyP["prevent_straight_wind"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x26 and messageBytes[cursor + 1] == 0x02) then
                keyP["auto_prevent_straight_wind"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x39 and messageBytes[cursor + 1] == 0x00) then
                keyP["self_clean"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x32 and messageBytes[cursor + 1] == 0x00) then
                if (messageBytes[cursor + 4] == 0x01) then keyP["wind_straight"] = 0x01 end
                if (messageBytes[cursor + 4] == 0x02) then
                    keyP["wind_avoid"] = 0x01
                    keyP["yb_wind_avoid"] = 0x02
                end
                if (messageBytes[cursor + 4] == 0x00) then
                    keyP["wind_straight"] = 0x00
                    keyP["wind_avoid"] = 0x00
                    keyP["yb_wind_avoid"] = 0x00
                end
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x33 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_avoid"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x34 and messageBytes[cursor + 1] == 0x00) then
                keyP["intelligent_wind"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x3A and messageBytes[cursor + 1] == 0x00) then
                keyP["child_prevent_cold_wind"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x18 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_no_wind_sense"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_no_wind_sense"] = 1
                    if (messageBytes[cursor + 3] == 0x02) then
                        keyP["fn_no_wind_sense"] = messageBytes[cursor + 4]
                        keyP["no_wind_sense_level"] = messageBytes[cursor + 5]
                        cursor = cursor + 6
                    else
                        keyP["no_wind_sense"] = messageBytes[cursor + 4]
                        cursor = cursor + 5
                    end
                end end
            if (messageBytes[cursor + 0] == 0x1B and messageBytes[cursor + 1] == 0x02) then
                keyP["little_angel"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x21 and messageBytes[cursor + 1] == 0x00) then
                keyP["cool_hot_sense"] = messageBytes[cursor + 4]
                cursor = cursor + 12
            end
            if (messageBytes[cursor + 0] == 0x29 and messageBytes[cursor + 1] == 0x00) then
                keyP["security"] = messageBytes[cursor + 4]
                if (messageBytes[cursor + 4] == 2) then keyP["security"] = 0 end
                if (messageBytes[cursor + 4] == 3) then keyP["security"] = 1 end
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x4E and messageBytes[cursor + 1] == 0x00) then
                keyP["even_wind"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x4F and messageBytes[cursor + 1] == 0x00) then
                keyP["single_tuyere"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x4C and messageBytes[cursor + 1] == 0x00) then
                keyP["extreme_wind"] = messageBytes[cursor + 4]
                keyP["extreme_wind_level"] = messageBytes[cursor + 5]
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x20 and messageBytes[cursor + 1] == 0x00) then
                keyP["voice_control"] = messageBytes[cursor + 4]
                keyP["voice_control_new"] = messageBytes[cursor + 4]
                cursor = cursor + 24
            end
            if (messageBytes[cursor + 0] == 0x01 and messageBytes[cursor + 1] == 0x02) then
                keyP["pre_cool_hot"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x4A and messageBytes[cursor + 1] == 0x00) then
                keyP["water_washing_manual"] = messageBytes[cursor + 4]
                keyP["water_washing"] = messageBytes[cursor + 5]
                keyP["water_washing_time"] = messageBytes[cursor + 6]
                keyP["water_washing_stage"] = messageBytes[cursor + 7]
                cursor = cursor + 8
            end
            if (messageBytes[cursor + 0] == 0x4B and messageBytes[cursor + 1] == 0x00) then
                keyP["fresh_air"] = messageBytes[cursor + 4]
                keyP["fresh_air_fan_speed"] = messageBytes[cursor + 5]
                keyP["fresh_air_temp"] = messageBytes[cursor + 6]
                keyP["fresh_air_mode_two"] = messageBytes[cursor + 7]
                cursor = cursor + 8
            end
            if (messageBytes[cursor + 0] == 0x51 and messageBytes[cursor + 1] == 0x00) then
                keyP["parent_control"] = messageBytes[cursor + 4]
                keyP["parent_control_temp_up"] = messageBytes[cursor + 5]
                keyP["parent_control_temp_down"] = messageBytes[cursor + 6]
                cursor = cursor + 9
            end
            if (messageBytes[cursor + 0] == 0x43 and messageBytes[cursor + 1] == 0x00) then
                if (messageBytes[cursor + 4] == 0x01 or messageBytes[cursor + 4] == 0x00) then
                    keyP["gentle_wind_sense"] = 0x01
                    keyP["fa_prevent_straight_wind"] = 0x01
                end
                if (messageBytes[cursor + 4] == 0x02) then
                    keyP["gentle_wind_sense"] = 0x01
                    keyP["fa_prevent_straight_wind"] = 0x02
                end
                if (messageBytes[cursor + 4] == 0x03) then keyP["gentle_wind_sense"] = 0x03 end
                if (messageBytes[cursor + 4] == 0x04) then keyP["gentle_wind_sense"] = 0x01 end
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x30 and messageBytes[cursor + 1] == 0x00) then
                keyP["nobody_energy_save"] = messageBytes[cursor + 4]
                cursor = cursor + 10
            end
            if (messageBytes[cursor + 0] == 0x09 and messageBytes[cursor + 1] == 0x04) then
                keyP["filter_level"] = messageBytes[cursor + 5]
                keyP["filter_value"] = messageBytes[cursor + 14]
                cursor = cursor + 17
            end
            if (messageBytes[cursor + 0] == 0x58 and messageBytes[cursor + 1] == 0x00) then
                keyP["prevent_straight_wind_lr"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x0B and messageBytes[cursor + 1] == 0x02) then
                keyP["pm25_value"] = messageBytes[cursor + 6] * 256 + messageBytes[cursor + 5]
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x50 and messageBytes[cursor + 1] == 0x00) then
                keyP["water_pump"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x31 and messageBytes[cursor + 1] == 0x00) then
                keyP["intelligent_control"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x24 and messageBytes[cursor + 1] == 0x00) then
                keyP["volume_control"] = messageBytes[cursor + 5]
                cursor = cursor + 8
            end
            if (messageBytes[cursor + 0] == 0x09 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_ud_angle"] = messageBytes[cursor + 4]
                keyP["left_ud_wind_angle"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x0A and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_lr_angle"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x44 and messageBytes[cursor + 1] == 0x00) then
                keyP["face_register"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x5A and messageBytes[cursor + 1] == 0x00) then
                keyP["degerming"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x5B and messageBytes[cursor + 1] == 0x00) then
                keyP["light"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xB5 and messageBytes[cursor + 1] == 0x00) then
                keyP["care_mode"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xB6 and messageBytes[cursor + 1] == 0x00) then
                keyP["care_mode_lock"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x61 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_top"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x59 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_around"] = messageBytes[cursor + 4]
                keyP["wind_around_ud"] = messageBytes[cursor + 5]
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x1A and messageBytes[cursor + 1] == 0x00) then cursor = cursor + 5 end
            if (messageBytes[cursor + 0] == 0x25 and messageBytes[cursor + 1] == 0x02) then
                keyP["cool_temp_down"] = messageBytes[cursor + 4]
                keyP["cool_temp_up"] = messageBytes[cursor + 5]
                keyP["auto_temp_down"] = messageBytes[cursor + 6]
                keyP["auto_temp_up"] = messageBytes[cursor + 7]
                keyP["heat_temp_down"] = messageBytes[cursor + 8]
                keyP["heat_temp_up"] = messageBytes[cursor + 9]
                cursor = cursor + 11
            end
            if (messageBytes[cursor + 0] == 0x27 and messageBytes[cursor + 1] == 0x02) then
                keyP["power_lock"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x29 and messageBytes[cursor + 1] == 0x02) then
                keyP["ptc_lock"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x2B and messageBytes[cursor + 1] == 0x02) then
                keyP["offline_operating_time"] = bit.bor(bit.lshift(messageBytes[cursor + 5], 8),
                    messageBytes[cursor + 4])
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x28 and messageBytes[cursor + 1] == 0x02) then
                keyP["operating_time"] = bit.bor(messageBytes[cursor + 4],
                    bit.bor(bit.lshift(messageBytes[cursor + 5], 8), bit.lshift(messageBytes[cursor + 6], 16)))
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x15 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then cursor =
                    cursor + 4 else
                    -- keyP["indoor_humidity"] = messageBytes[cursor + 4]  -- use C1/0x45 instead
                    cursor = cursor + 5
                end end
            if (messageBytes[cursor + 0] == 0x5C and messageBytes[cursor + 1] == 0x00) then
                keyP["child_lock"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x2C and messageBytes[cursor + 1] == 0x02) then
                keyP["buzzer_all"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x5D and messageBytes[cursor + 1] == 0x00) then
                keyP["self_remove_odor_phase"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x5E and messageBytes[cursor + 1] == 0x00) then
                keyP["high_temp_remove_odor_alone"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x5F and messageBytes[cursor + 1] == 0x00) then
                keyP["ozone"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x63 and messageBytes[cursor + 1] == 0x00) then
                keyP["soft_warm"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x50 and messageBytes[cursor + 1] == 0x02) then
                keyP["fresh_air_parm"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x67 and messageBytes[cursor + 1] == 0x00) then
                keyP["jet_cool"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x68 and messageBytes[cursor + 1] == 0x00) then
                keyP["rewarming_dry"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x69 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_arom"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_arom"] = 1
                    keyP["arom"] = messageBytes[cursor + 4]
                    keyP["arom_fan_speed"] = messageBytes[cursor + 5]
                    keyP["arom_time_clean"] = messageBytes[cursor + 6]
                    keyP["arom_time"] = bit.bor(bit.lshift(messageBytes[cursor + 8], 8), messageBytes[cursor + 7])
                    keyP["arom_time_total"] = bit.bor(bit.lshift(messageBytes[cursor + 10], 8), messageBytes[cursor + 9])
                    cursor = cursor + 11
                end end
            if (messageBytes[cursor + 0] == 0x01 and messageBytes[cursor + 1] == 0x00) then
                keyP["new_mode_power"] = messageBytes[cursor + 4]
                keyP["new_mode"] = messageBytes[cursor + 5]
                keyP["new_temperature"] = messageBytes[cursor + 6] / 2
                keyP["new_wind_speed"] = messageBytes[cursor + 7]
                cursor = cursor + 8
            end
            if (messageBytes[cursor + 0] == 0x30 and messageBytes[cursor + 1] == 0x02) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_guide_strip"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_guide_strip"] = 1
                    keyP["main_horizontal_guide_strip_1"] = messageBytes[cursor + 4]
                    keyP["main_horizontal_guide_strip_2"] = messageBytes[cursor + 5]
                    keyP["main_horizontal_guide_strip_3"] = messageBytes[cursor + 6]
                    keyP["main_horizontal_guide_strip_4"] = messageBytes[cursor + 7]
                    cursor = cursor + 8
                end end
            if (messageBytes[cursor + 0] == 0x6F and messageBytes[cursor + 1] == 0x00) then
                keyP["uvc_remove_odor"] = messageBytes[cursor + 4]
                keyP["uvc_power_off"] = messageBytes[cursor + 5]
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x08 and messageBytes[cursor + 1] == 0x02) then
                keyP["light_sensitive"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x71 and messageBytes[cursor + 1] == 0x00) then
                keyP["whirl_wind_left"] = messageBytes[cursor + 4]
                keyP["whirl_wind_right"] = messageBytes[cursor + 5]
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x70 and messageBytes[cursor + 1] == 0x00) then
                keyP["inner_purifier"] = messageBytes[cursor + 4]
                keyP["inner_purifier_fan_speed"] = messageBytes[cursor + 5]
                keyP["inner_purifier_mode"] = messageBytes[cursor + 6]
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x73 and messageBytes[cursor + 1] == 0x00) then
                keyP["indoor_co2"] = bit.bor(bit.lshift(messageBytes[cursor + 5], 8), messageBytes[cursor + 4])
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x77 and messageBytes[cursor + 1] == 0x00) then
                keyP["remove_odor"] = messageBytes[cursor + 4]
                keyP["remove_odor_fan_speed"] = messageBytes[cursor + 5]
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x76 and messageBytes[cursor + 1] == 0x00) then
                keyP["fresh_air_on_co2"] = bit.bor(bit.lshift(messageBytes[cursor + 5], 8), messageBytes[cursor + 4])
                keyP["fresh_air_off_co2"] = bit.bor(bit.lshift(messageBytes[cursor + 7], 8), messageBytes[cursor + 6])
                cursor = cursor + 8
            end
            if (messageBytes[cursor + 0] == 0x7B and messageBytes[cursor + 1] == 0x00) then
                keyP["linkage"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x7C and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_moisturizing"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_moisturizing"] = 1
                    keyP["moisturizing"] = messageBytes[cursor + 4]
                    keyP["moisturizing_fan_speed"] = messageBytes[cursor + 5]
                    cursor = cursor + 6
                end end
            if (messageBytes[cursor + 0] == 0x74 and messageBytes[cursor + 1] == 0x00) then
                keyP["no_wind_sense_left"] = messageBytes[cursor + 4]
                keyP["no_wind_sense_right"] = messageBytes[cursor + 5]
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x7F and messageBytes[cursor + 1] == 0x00) then
                keyP["powerValue"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x02 and messageBytes[cursor + 1] == 0x00) then
                keyP["modeValue"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x03 and messageBytes[cursor + 1] == 0x00) then
                keyP["temperature"] = (messageBytes[cursor + 4] - 50) / 2
                keyP["smallTemperature"] = (messageBytes[cursor + 4] - 50) % 2
                if (keyP["smallTemperature"] == 0) then keyP["smallTemperature"] = 1 end
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x06 and messageBytes[cursor + 1] == 0x00) then
                keyP["fanspeedValue"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x80 and messageBytes[cursor + 1] == 0x00) then
                keyP["swingLRValue"] = messageBytes[cursor + 4]
                keyP["wind_swing_lr_left"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x81 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_lr_right"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x82 and messageBytes[cursor + 1] == 0x00) then
                keyP["swingUDValue"] = messageBytes[cursor + 4]
                keyP["wind_swing_ud_left"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x83 and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_ud_right"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x84 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then cursor =
                    cursor + 4 else
                    keyP["wind_speed_right"] = messageBytes[cursor + 4]
                    cursor = cursor + 5
                end end
            if (messageBytes[cursor + 0] == 0x10 and messageBytes[cursor + 1] == 0x00) then
                keyP["dryValue"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x17 and messageBytes[cursor + 1] == 0x00) then
                keyP["screen_display"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x0F and messageBytes[cursor + 1] == 0x00) then
                keyP["PTCValue"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x11 and messageBytes[cursor + 1] == 0x02) then
                keyP["ptc_default_rule"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x85 and messageBytes[cursor + 1] == 0x00) then
                keyP["fresh_filter_reset"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x0D and messageBytes[cursor + 1] == 0x00) then
                keyP["ecoValue"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x0B and messageBytes[cursor + 1] == 0x00) then
                keyP["openTimerSwitch"] = messageBytes[cursor + 4]
                keyP["openHour"] = messageBytes[cursor + 5]
                keyP["openStepMintues"] = messageBytes[cursor + 6]
                keyP["openTime"] = keyP["openHour"] * 60 + keyP["openStepMintues"]
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x0C and messageBytes[cursor + 1] == 0x00) then
                keyP["closeTimerSwitch"] = messageBytes[cursor + 4]
                keyP["closeHour"] = messageBytes[cursor + 5]
                keyP["closeStepMintues"] = messageBytes[cursor + 6]
                keyP["closeTime"] = keyP["closeHour"] * 60 + keyP["closeStepMintues"]
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x11 and messageBytes[cursor + 1] == 0x00) then
                keyP["comfortableSleepValue"] = messageBytes[cursor + 4]
                if (keyP["comfortableSleepValue"] == 0x01) then keyP["comfortableSleepValue"] = 0x03 end
                cursor = cursor + 16
            end
            if (messageBytes[cursor + 0] == 0x86 and messageBytes[cursor + 1] == 0x00) then
                keyP["gentle_wind_sense"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x22 and messageBytes[cursor + 1] == 0x00) then
                keyP["comfortPowerSave"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x87 and messageBytes[cursor + 1] == 0x00) then
                keyP["screen_display_time"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x88 and messageBytes[cursor + 1] == 0x00) then
                keyP["total_status_switch"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x99 and messageBytes[cursor + 1] == 0x00) then
                keyP["wait_clean"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x9A and messageBytes[cursor + 1] == 0x00) then
                keyP["self_clean_stage"] = bit.band(messageBytes[cursor + 4], 0x01)
                keyP["self_clean_time"] = bit.rshift(bit.band(messageBytes[cursor + 4], 0x02), 1)
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x9B and messageBytes[cursor + 1] == 0x00) then
                keyP["dry_clean_stage"] = bit.band(messageBytes[cursor + 4], 0x01)
                keyP["dry_clean_time"] = bit.rshift(bit.band(messageBytes[cursor + 4], 0x02), 1)
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x07 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_left_down_real_wind_speed"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_left_down_real_wind_speed"] = 1
                    keyP["left_down_real_wind_speed"] = messageBytes[cursor + 4]
                    cursor = cursor + 5
                end end
            if (messageBytes[cursor + 0] == 0xA4 and messageBytes[cursor + 1] == 0x00) then
                keyP["right_up_real_wind_speed"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xA0 and messageBytes[cursor + 1] == 0x00) then
                keyP["ptc_load"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x9F and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_no_wind_sense_judge_param"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_no_wind_sense_judge_param"] = 1
                    keyP["no_wind_sense_judge_param"] = messageBytes[cursor + 4]
                    cursor = cursor + 5
                end end
            if (messageBytes[cursor + 0] == 0x0A and messageBytes[cursor + 1] == 0x00) then
                keyP["up_lr_wind_angle"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x96 and messageBytes[cursor + 1] == 0x00) then
                keyP["swing_lr_under_angle"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xA1 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_right_ud_wind_angle"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_right_ud_wind_angle"] = 1
                    keyP["right_ud_wind_angle"] = messageBytes[cursor + 4]
                    cursor = cursor + 5
                end end
            if (messageBytes[cursor + 0] == 0xA2 and messageBytes[cursor + 1] == 0x00) then
                keyP["left_lr_wind_angle"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xA3 and messageBytes[cursor + 1] == 0x00) then
                keyP["right_lr_wind_angle"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xA8 and messageBytes[cursor + 1] == 0x00) then
                keyP["defrosting_load"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xB2 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] ~= 0x00 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_linkage_2"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_linkage_2"] = 1
                    keyP["linkage_2"] = messageBytes[cursor + 4]
                    cursor = cursor + 5
                end end
            if (messageBytes[cursor + 0] == 0xB3 and messageBytes[cursor + 1] == 0x00) then
                keyP["quick_cool_heat"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x78 and messageBytes[cursor + 1] == 0x00) then
                keyP["auto_prevent_cold_wind"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x79 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_wind_swing_ud_angle_diy"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_wind_swing_ud_angle_diy"] = 1
                    keyP["wind_swing_ud_angle_up"] = messageBytes[cursor + 4]
                    keyP["wind_swing_ud_angle_down"] = messageBytes[cursor + 5]
                    keyP["app_control_remember_ud"] = messageBytes[cursor + 6]
                    cursor = cursor + 7
                end end
            if (messageBytes[cursor + 0] == 0x7A and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_wind_swing_lr_angle_diy"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_wind_swing_lr_angle_diy"] = 1
                    keyP["wind_swing_lr_angle_up"] = messageBytes[cursor + 4]
                    keyP["wind_swing_lr_angle_down"] = messageBytes[cursor + 5]
                    keyP["app_control_remember_lr"] = messageBytes[cursor + 6]
                    cursor = cursor + 7
                end end
            if (messageBytes[cursor + 0] == 0xE2 and messageBytes[cursor + 1] == 0x00) then
                keyP["real_mode"] = messageBytes[cursor + 16]
                keyP["left_down_real_wind_speed"] = messageBytes[cursor + 16]
                keyP["right_up_real_wind_speed"] = messageBytes[cursor + 46]
                keyP["defrosting_load"] = bit.band(messageBytes[cursor + 17], 0x01)
                keyP["ptc_load"] = bit.rshift(bit.band(messageBytes[cursor + 17], 0x02), 1)
                keyP["self_clean_stage"] = messageBytes[cursor + 43]
                keyP["self_clean_time"] = messageBytes[cursor + 44]
                keyP["dry_clean_stage"] = bit.rshift(bit.band(messageBytes[cursor + 45], 0x80), 7)
                keyP["dry_clean_time"] = bit.band(messageBytes[cursor + 45], 0x7F)
                cursor = cursor + messageBytes[cursor + 3] + 4
            end
            if (messageBytes[cursor + 0] == 0xE1 and messageBytes[cursor + 1] == 0x00) then cursor = cursor +
                messageBytes[cursor + 3] + 4 end
            if (messageBytes[cursor + 0] == 0xE0 and messageBytes[cursor + 1] == 0x00) then
                keyP["outdoor_temperature"] = messageBytes[cursor + 14] * 256 + messageBytes[cursor + 13]
                if (keyP["outdoor_temperature"] > 32767) then keyP["outdoor_temperature"] = keyP["outdoor_temperature"] -
                    65535 - 1 end
                cursor = cursor + messageBytes[cursor + 3] + 4
            end
            if (messageBytes[cursor + 0] == 0x14 and messageBytes[cursor + 1] == 0x00) then
                keyP["smart_dry_value"] = messageBytes[cursor + 4]
                cursor = cursor + messageBytes[cursor + 3] + 4
            end
            if (messageBytes[cursor + 0] == 0xAE and messageBytes[cursor + 1] == 0x00) then
                keyP["wind_swing_lr_under"] = messageBytes[cursor + 4]
                cursor = cursor + messageBytes[cursor + 3] + 4
            end
            if (messageBytes[cursor + 0] == 0x36 and messageBytes[cursor + 1] == 0x02) then
                keyP["screen_display_select"] = messageBytes[cursor + 4]
                cursor = cursor + messageBytes[cursor + 3] + 4
            end
            if (messageBytes[cursor + 0] == 0xAF and messageBytes[cursor + 1] == 0x00) then
                keyP["no_wind_sense_up"] = messageBytes[cursor + 4]
                keyP["no_wind_sense_down"] = messageBytes[cursor + 5]
                cursor = cursor + messageBytes[cursor + 3] + 4
            end
            if (messageBytes[cursor + 0] == 0x89 and messageBytes[cursor + 1] == 0x00) then
                keyP["cool_power_saving"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x54 and messageBytes[cursor + 1] == 0x02) then
                keyP["prepare_food"] = messageBytes[cursor + 4]
                keyP["prepare_food_temp"] = messageBytes[cursor + 5]
                keyP["prepare_food_fan_speed"] = messageBytes[cursor + 6]
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x55 and messageBytes[cursor + 1] == 0x02) then
                keyP["quick_fry"] = messageBytes[cursor + 4]
                keyP["quick_fry_temp"] = messageBytes[cursor + 5]
                keyP["quick_fry_fan_speed"] = messageBytes[cursor + 6]
                cursor = cursor + 7
            end
            if (messageBytes[cursor + 0] == 0x8B and messageBytes[cursor + 1] == 0x00) then
                keyP["quick_fry_center_point"] = messageBytes[cursor + 4]
                keyP["quick_fry_angle"] = messageBytes[cursor + 5]
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0xB8 and messageBytes[cursor + 1] == 0x00) then
                keyP["dust_full_time_reset"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x62 and messageBytes[cursor + 1] == 0x00) then
                keyP["power_saving"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x38 and messageBytes[cursor + 1] == 0x02) then
                keyP["prevent_straight_wind_distance"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0x62 and messageBytes[cursor + 1] == 0x00) then
                keyP["power_saving"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xB9 and messageBytes[cursor + 1] == 0x00) then
                keyP["circle_fan"] = messageBytes[cursor + 4]
                keyP["circle_fan_mode"] = messageBytes[cursor + 5]
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0x2F and messageBytes[cursor + 1] == 0x02) then
                keyP["buzzer_off_status"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xbF and messageBytes[cursor + 1] == 0x00) then
                keyP["air_remove_odor"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xC7 and messageBytes[cursor + 1] == 0x00) then
                keyP["clean_breath"] = messageBytes[cursor + 4]
                keyP["clean_breath_level"] = messageBytes[cursor + 5]
                cursor = cursor + 6
            end
            if (messageBytes[cursor + 0] == 0xC8 and messageBytes[cursor + 1] == 0x00) then
                keyP["remove_arofene_clean"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xC9 and messageBytes[cursor + 1] == 0x00) then
                keyP["health"] = messageBytes[cursor + 4]
                cursor = cursor + 5
            end
            if (messageBytes[cursor + 0] == 0xB7 and messageBytes[cursor + 1] == 0x00) then
                keyP["breath_cool"] = bit.band(messageBytes[cursor + 4], 0x01)
                keyP["breath_heat"] = bit.rshift(bit.band(messageBytes[cursor + 4], 0x02), 1)
                keyP["breath_remove_odor"] = bit.rshift(bit.band(messageBytes[cursor + 4], 0x08), 3)
                keyP["breath_fresh_air"] = bit.rshift(bit.band(messageBytes[cursor + 4], 0x10), 4)
                keyP["breath_purifier"] = bit.rshift(bit.band(messageBytes[cursor + 4], 0x20), 5)
                keyP["cool_light_color_r"] = messageBytes[cursor + 5]
                keyP["cool_light_color_g"] = messageBytes[cursor + 6]
                keyP["cool_light_color_b"] = messageBytes[cursor + 7]
                keyP["heat_light_color_r"] = messageBytes[cursor + 8]
                keyP["heat_light_color_g"] = messageBytes[cursor + 9]
                keyP["heat_light_color_b"] = messageBytes[cursor + 10]
                keyP["dry_light_color_r"] = messageBytes[cursor + 11]
                keyP["dry_light_color_g"] = messageBytes[cursor + 12]
                keyP["dry_light_color_b"] = messageBytes[cursor + 13]
                keyP["remove_odor_light_color_r"] = messageBytes[cursor + 14]
                keyP["remove_odor_light_color_g"] = messageBytes[cursor + 15]
                keyP["remove_odor_light_color_b"] = messageBytes[cursor + 16]
                keyP["fresh_light_color_r"] = messageBytes[cursor + 17]
                keyP["fresh_light_color_g"] = messageBytes[cursor + 18]
                keyP["fresh_light_color_b"] = messageBytes[cursor + 19]
                keyP["purifier_light_color_r"] = messageBytes[cursor + 20]
                keyP["purifier_light_color_g"] = messageBytes[cursor + 21]
                keyP["purifier_light_color_b"] = messageBytes[cursor + 22]
                cursor = cursor + 23
            end
            if (messageBytes[cursor + 0] == 0xE3 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_ieco"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_ieco"] = 1
                    keyP["ieco_number"] = messageBytes[cursor + 4]
                    keyP["ieco_switch"] = messageBytes[cursor + 5]
                    cursor = cursor + 6
                end end
            if (messageBytes[cursor + 0] == 0xBC and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_auto_prevent_cold_wind_memory"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_auto_prevent_cold_wind_memory"] = 1
                    keyP["auto_prevent_cold_wind_memory"] = messageBytes[cursor + 4]
                    cursor = cursor + 5
                end end
            if (messageBytes[cursor + 0] == 0x1E and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_eco_time"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_eco_time"] = 1
                    keyP["eco_time_switch"] = messageBytes[cursor + 5]
                    keyP["eco_time_sec"] = messageBytes[cursor + 5]
                    keyP["eco_time_min"] = messageBytes[cursor + 6]
                    keyP["eco_time_hour"] = messageBytes[cursor + 7]
                    cursor = cursor + messageBytes[cursor + 3] + 4
                end end
            if (messageBytes[cursor + 0] == 0xCA and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_strong_cool"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_strong_cool"] = 1
                    keyP["strong_cool"] = messageBytes[cursor + 4]
                    cursor = cursor + messageBytes[cursor + 3] + 4
                end end
            if (messageBytes[cursor + 0] == 0x75 and messageBytes[cursor + 1] == 0x00) then if (messageBytes[cursor + 2] == 0x11 or messageBytes[cursor + 2] == 0x10 or messageBytes[cursor + 3] == 0x00) then
                    keyP["has_humidification"] = 0
                    cursor = cursor + 4
                else
                    keyP["has_humidification"] = 1
                    keyP["humidification"] = messageBytes[cursor + 4]
                    keyP["humidification_fan_speed"] = messageBytes[cursor + 5]
                    keyP["humidification_mode"] = messageBytes[cursor + 6]
                    cursor = cursor + messageBytes[cursor + 3] + 4
                end end
            if (messageBytes[cursor + 0] == 0x7E and messageBytes[cursor + 1] == 0x00) then
                if ((function(t)
                        local c = 0; for _ in pairs(t) do c = c + 1 end
                        return c
                    end)(binData) < 21) then return nil end
                keyP["analysis_value"] =
                "power,mode,temperature,wind_speed,power_on_timer,smart_dry_value,power_off_timer,power_off_time_value,power_on_time_value,ptc,eco,dry,wind_swing_lr,wind_swing_lr_under,wind_swing_ud,kick_quilt,prevent_cold,small_temperature,purifier,dust_full_time,power_saving,fault_tag,wind_swing_ud_left,wind_swing_ud_right,wind_swing_lr_right,wind_swing_lr_left,wind_swing_ud_angle,wind_swing_lr_angle,screen_display_select,swing_lr_under_angle,screen_display_now,screen_display,auto_prevent_cold_wind,no_wind_sense_up,no_wind_sense_down,voice_control_new,voice_control,soft_warm"
                keyP["powerValue"] = bit.band(messageBytes[cursor + 5], 0x01)
                keyP["modeValue"] = bit.band(messageBytes[cursor + 6], 0xE0)
                if (keyP["modeValue"] == 0x20) then keyP["modeValue"] = 1 elseif (keyP["modeValue"] == 0x40) then keyP["modeValue"] = 2 elseif (keyP["modeValue"] == 0x60) then keyP["modeValue"] = 3 elseif (keyP["modeValue"] == 0x80) then keyP["modeValue"] = 4 elseif (keyP["modeValue"] == 0xA0) then keyP["modeValue"] = 5 elseif (keyP["modeValue"] == 0xC0) then keyP["modeValue"] = 6 end
                if (messageBytes[cursor + 4] == 0xA0) then if deviceSN8 == "11447" or deviceSN8 == "11451" or deviceSN8 == "11453" or deviceSN8 == "11455" or deviceSN8 == "11457" or deviceSN8 == "11459" or deviceSN8 == "11525" or deviceSN8 == "11527" or deviceSN8 == "11533" or deviceSN8 == "11535" then
                        keyP["temperature"] = bit.rshift(bit.band(messageBytes[cursor + 5], 0x7C), 2) + 0x0C
                        keyP["smallTemperature"] = bit.rshift(bit.band(messageBytes[cursor + 5], 0x02), 1)
                    else
                        keyP["temperature"] = bit.rshift(bit.band(messageBytes[cursor + 5], 0x3E), 1) + 0x0C
                        keyP["smallTemperature"] = bit.rshift(bit.band(messageBytes[cursor + 5], 0x40), 6)
                    end end
                keyP["fanspeedValue"] = bit.band(messageBytes[cursor + 7], 0x7F)
                if (bit.band(messageBytes[cursor + 8], keyB["BYTE_START_TIMER_SWITCH_ON"]) == keyB["BYTE_START_TIMER_SWITCH_ON"]) then keyP["openTimerSwitch"] =
                    keyB["BYTE_START_TIMER_SWITCH_ON"] else keyP["openTimerSwitch"] = keyB
                    ["BYTE_START_TIMER_SWITCH_OFF"] end
                if (bit.band(messageBytes[cursor + 9], keyB["BYTE_CLOSE_TIMER_SWITCH_ON"]) == keyB["BYTE_CLOSE_TIMER_SWITCH_ON"]) then keyP["closeTimerSwitch"] =
                    keyB["BYTE_CLOSE_TIMER_SWITCH_ON"] else keyP["closeTimerSwitch"] = keyB
                    ["BYTE_CLOSE_TIMER_SWITCH_OFF"] end
                keyP["closeHour"] = bit.rshift(bit.band(messageBytes[cursor + 9], 0x7F), 2)
                keyP["closeStepMintues"] = bit.band(messageBytes[cursor + 9], 0x03)
                keyP["closeMin"] = 15 - bit.band(messageBytes[cursor + 10], 0x0f)
                keyP["closeTime"] = keyP["closeHour"] * 60 + keyP["closeStepMintues"] * 15 + keyP["closeMin"]
                keyP["openHour"] = bit.rshift(bit.band(messageBytes[cursor + 8], 0x7F), 2)
                keyP["openStepMintues"] = bit.band(messageBytes[cursor + 8], 0x03)
                keyP["openMin"] = 15 - bit.rshift(bit.band(messageBytes[cursor + 10], 0xf0), 4)
                keyP["openTime"] = keyP["openHour"] * 60 + keyP["openStepMintues"] * 15 + keyP["openMin"]
                keyP["strongWindValue"] = bit.band(messageBytes[cursor + 12], 0x20)
                keyP["power_saving"] = bit.band(messageBytes[cursor + 12], 0x08)
                keyP["comfortableSleepValue"] = bit.band(messageBytes[cursor + 12], 0x03)
                keyP["comfortableSleepSwitch"] = bit.band(messageBytes[cursor + 12], 0x40)
                if (messageBytes[cursor + 4] == 0xA0) then
                    keyP["comfortableSleepSwitch"] = bit.band(messageBytes[cursor + 18], 0x01)
                    keyP["naturalWind"] = bit.band(messageBytes[cursor + 14], 0x40)
                    keyP["screenDisplayNowValue"] = bit.band(messageBytes[cursor + 15], 0x07)
                    keyP["pmv"] = bit.rshift(bit.band(messageBytes[cursor + 15], 0xF0), 4) * 0.5 - 3.5
                    keyP["swingLRValueUnder"] = bit.band(messageBytes[cursor + 13], 0x40)
                end
                keyP["PTCValue"] = bit.band(messageBytes[cursor + 13], 0x08)
                keyP["purifierValue"] = bit.band(messageBytes[cursor + 13], 0x20)
                keyP["inner_purifier"] = bit.rshift(bit.band(messageBytes[cursor + 13], 0x20), 5)
                keyP["ecoValue"] = bit.lshift(bit.band(messageBytes[cursor + 13], 0x10), 3)
                keyP["dryValue"] = bit.band(messageBytes[cursor + 13], 0x04)
                if (keyP["dryValue"] == 0x04) then keyP["dryValue"] = 1 end
                keyP["swingLRValue"] = bit.band(messageBytes[cursor + 11], 0x03)
                if (keyP["swingLRValue"] == 0x03) then keyP["swingLRValue"] = 1 end
                keyP["wind_swing_lr_right"] = bit.band(messageBytes[cursor + 11], 0x01)
                keyP["wind_swing_lr_left"] = bit.band(messageBytes[cursor + 11], 0x02)
                if (keyP["wind_swing_lr_left"] == 0x02) then keyP["wind_swing_lr_left"] = 1 end
                keyP["swingUDValue"] = bit.band(messageBytes[cursor + 11], 0x0C)
                if (keyP["swingUDValue"] == 0x0C) then keyP["swingUDValue"] = 1 end
                keyP["wind_swing_ud_right"] = bit.band(messageBytes[cursor + 11], 0x04)
                if (keyP["wind_swing_ud_right"] == 0x04) then keyP["wind_swing_ud_right"] = 1 end
                keyP["wind_swing_ud_left"] = bit.band(messageBytes[cursor + 11], 0x08)
                if (keyP["wind_swing_ud_left"] == 0x08) then keyP["wind_swing_ud_left"] = 1 end
                keyP["swingLRUnderSwitch"] = bit.band(messageBytes[cursor + 23], 0x80)
                keyP["errorCode"] = messageBytes[cursor + 20]
                keyP["kickQuilt"] = bit.rshift(bit.band(messageBytes[cursor + 14], 0x04), 2)
                keyP["preventCold"] = bit.rshift(bit.band(messageBytes[cursor + 14], 0x08), 3)
                local temp = bit.rshift(bit.band(messageBytes[cursor + 16], 0x3E), 1)
                if (temp > 0 and temp <= 25) then keyP["temperature"] = temp + 12 end
                if (messageBytes[cursor + 4] == 0xA0) then
                    keyP["arom_old"] = bit.rshift(bit.band(messageBytes[cursor + 25], 0x80), 7)
                    keyP["analysis_value"] = keyP["analysis_value"] .. ",arom_old"
                end
                keyP["soft_warm"] = bit.rshift(bit.band(messageBytes[cursor + 24], 0x02), 1)
                keyP["wind_around"] = bit.rshift(bit.band(messageBytes[cursor + 11], 0x80), 7)
                keyP["dust_full_time"] = bit.rshift(bit.band(messageBytes[cursor + 11], 0x40), 6)
                keyP["wind_around_ud"] = bit.rshift(bit.band(messageBytes[cursor + 25], 0x18), 3)
                keyP["prevent_straight_wind_lr"] = bit.rshift(bit.band(messageBytes[cursor + 25], 0x60), 5)
                keyP["comfortPowerSave"] = bit.band(messageBytes[cursor + 18], 0x01)
                keyP["analysis_value"] = keyP["analysis_value"] .. ",comfort_power_save"
                keyP["rewarming_dry"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0x02), 1)
                keyP["no_wind_sense_up"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0x04), 2)
                keyP["no_wind_sense_down"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0x08), 3)
                if (keyP["no_wind_sense_up"] == 1) then keyP["no_wind_sense_up"] = 2 else keyP["no_wind_sense_up"] = 1 end
                if (keyP["no_wind_sense_down"] == 1) then keyP["no_wind_sense_down"] = 2 else keyP["no_wind_sense_down"] = 1 end
                if (#binData >= 24) then
                    keyP["wind_speed_right"] = bit.band(messageBytes[cursor + 28], 0x7F)
                    keyP["analysis_value"] = keyP["analysis_value"] .. ",wind_speed_right"
                end
                if (#binData >= 26) then
                    keyP["indoor_co2"] = bit.bor(bit.lshift(messageBytes[cursor + 30], 8), messageBytes[cursor + 29])
                    keyP["whirl_wind_right"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x08), 3)
                    keyP["whirl_wind_left"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x04), 2)
                end
                keyP["analysis_value"] = keyP["analysis_value"] ..
                ",wind_swing_lr_angle,wind_swing_ud_angle,gentle_wind_sense,prevent_straight_wind,no_wind_sense,fresh_air,linkage_sync,linkage,moisturizing,no_wind_sense_right,no_wind_sense_left,ptc_default_rule,light_sensitive,self_clean,prevent_super_cool,cool_power_saving,prepare_food,quick_fry"
                keyP["self_clean"] = bit.rshift(bit.band(messageBytes[cursor + 12], 0x04), 2)
                keyP["prevent_super_cool"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x40), 6)
                keyP["no_wind_sense_left"] = bit.band(messageBytes[cursor + 31], 0x01) + 1
                keyP["no_wind_sense_right"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x02), 1) + 1
                keyP["moisturizing"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x80), 7)
                keyP["linkage"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x20), 5)
                keyP["linkage_sync"] = bit.rshift(bit.band(messageBytes[cursor + 31], 0x40), 6)
                keyP["smart_dry_value"] = messageBytes[cursor + 17]
                keyP["no_wind_sense"] = bit.rshift(bit.band(messageBytes[cursor + 18], 0x08), 3)
                keyP["prevent_straight_wind"] = bit.rshift(bit.band(messageBytes[cursor + 18], 0x40), 6)
                if (keyP["prevent_straight_wind"] == 1) then keyP["prevent_straight_wind"] = 2 end
                if (keyP["prevent_straight_wind"] == 0) then keyP["prevent_straight_wind"] = 1 end
                keyP["gentle_wind_sense"] = bit.band(messageBytes[cursor + 22], 0x01)
                keyP["auto_prevent_cold_wind"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x20), 5)
                keyP["wind_swing_ud_angle"] = bit.band(messageBytes[cursor + 21], 0x0F)
                keyP["degerming"] = bit.rshift(bit.band(messageBytes[cursor + 23], 0x02), 1)
                keyP["remove_odor"] = bit.rshift(bit.band(messageBytes[cursor + 23], 0x02), 1)
                if (keyP["wind_swing_ud_angle"] == 2) then keyP["wind_swing_ud_angle"] = 13 elseif (keyP["wind_swing_ud_angle"] == 3) then keyP["wind_swing_ud_angle"] = 25 elseif (keyP["wind_swing_ud_angle"] == 4) then keyP["wind_swing_ud_angle"] = 38 elseif (keyP["wind_swing_ud_angle"] == 5) then keyP["wind_swing_ud_angle"] = 50 elseif (keyP["wind_swing_ud_angle"] == 6) then keyP["wind_swing_ud_angle"] = 62 elseif (keyP["wind_swing_ud_angle"] == 7) then keyP["wind_swing_ud_angle"] = 75 elseif (keyP["wind_swing_ud_angle"] == 8) then keyP["wind_swing_ud_angle"] = 88 elseif (keyP["wind_swing_ud_angle"] == 9) then keyP["wind_swing_ud_angle"] = 100 end
                keyP["left_ud_wind_angle"] = keyP["wind_swing_ud_angle"]
                keyP["wind_swing_lr_angle"] = bit.rshift(bit.band(messageBytes[cursor + 21], 0xF0), 4)
                if (keyP["wind_swing_lr_angle"] == 2) then keyP["wind_swing_lr_angle"] = 13 elseif (keyP["wind_swing_lr_angle"] == 3) then keyP["wind_swing_lr_angle"] = 25 elseif (keyP["wind_swing_lr_angle"] == 4) then keyP["wind_swing_lr_angle"] = 38 elseif (keyP["wind_swing_lr_angle"] == 5) then keyP["wind_swing_lr_angle"] = 50 elseif (keyP["wind_swing_lr_angle"] == 6) then keyP["wind_swing_lr_angle"] = 62 elseif (keyP["wind_swing_lr_angle"] == 7) then keyP["wind_swing_lr_angle"] = 75 elseif (keyP["wind_swing_lr_angle"] == 8) then keyP["wind_swing_lr_angle"] = 88 elseif (keyP["wind_swing_lr_angle"] == 9) then keyP["wind_swing_lr_angle"] = 100 end
                keyP["left_lr_wind_angle"] = keyP["wind_swing_lr_angle"]
                if (messageBytes[cursor + 3] >= 33) then
                    keyP["fresh_air_mode_two"] = bit.band(messageBytes[cursor + 37], 0x0F)
                    keyP["fresh_air_mode"] = bit.rshift(bit.band(messageBytes[cursor + 37], 0x30), 4)
                    if (keyP["fresh_air_mode"] == 1) then keyP["fresh_air_mode"] = 0 elseif (keyP["fresh_air_mode"] == 3) then keyP["fresh_air_mode"] = 1 end
                    keyP["inner_purifier_mode"] = bit.rshift(bit.band(messageBytes[cursor + 37], 0x40), 6)
                    keyP["cool_power_saving"] = bit.rshift(bit.band(messageBytes[cursor + 37], 0x80), 7)
                    keyP["moisturizing_fan_speed"] = messageBytes[cursor + 36]
                    keyP["fresh_air_fan_speed"] = messageBytes[cursor + 38]
                    keyP["inner_purifier_fan_speed"] = messageBytes[cursor + 39]
                    -- keyP["indoor_humidity"] = messageBytes[cursor + 40]  -- use C1/0x45 instead
                    keyP["five_dimension_mode"] = bit.band(messageBytes[cursor + 41], 0x03)
                    keyP["total_status_switch"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x04), 2)
                    keyP["wind_no_linkage"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x10), 4)
                    keyP["jet_cool"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x08), 3)
                    keyP["quick_fry"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x20), 5)
                    keyP["prepare_food"] = bit.rshift(bit.band(messageBytes[cursor + 41], 0x40), 6)
                end
                if (messageBytes[cursor + 3] > 38) then
                    keyP["screen_display_time"] = messageBytes[cursor + 43]
                    keyP["strong_cool"] = bit.rshift(bit.band(messageBytes[cursor + 42], 0x80), 7)
                    keyP["linkage_fan_speed"] = bit.band(messageBytes[cursor + 42], 0x7F)
                    keyP["indoorTemperatureValue"] = (messageBytes[cursor + 44] - 50) / 2
                    keyP["smallIndoorTemperatureValue"] = bit.band(messageBytes[cursor + 45], 0x0F)
                    keyP["ieco_switch"] = bit.rshift(bit.band(messageBytes[cursor + 45], 0x10), 4)
                    keyP["analysis_value"] = keyP["analysis_value"] ..
                    ",screen_display_time,linkage_fan_speed,indoor_temperature,ieco_switch"
                end
                if (messageBytes[cursor + 3] > 41) then
                    keyP["no_wind_sense_judge_param"] = bit.rshift(bit.band(messageBytes[cursor + 45], 0x80), 7)
                    keyP["wait_clean"] = bit.rshift(bit.band(messageBytes[cursor + 45], 0x40), 6)
                end
                if (messageBytes[cursor + 3] > 42) then keyP["quick_fry_center_point"] = messageBytes[cursor + 46] end
                if (messageBytes[cursor + 3] > 43) then
                    keyP["right_ud_wind_angle"] = bit.band(messageBytes[cursor + 47], 0x0F)
                    if (keyP["right_ud_wind_angle"] == 2) then keyP["right_ud_wind_angle"] = 13 elseif (keyP["right_ud_wind_angle"] == 3) then keyP["right_ud_wind_angle"] = 25 elseif (keyP["right_ud_wind_angle"] == 4) then keyP["right_ud_wind_angle"] = 38 elseif (keyP["right_ud_wind_angle"] == 5) then keyP["right_ud_wind_angle"] = 50 elseif (keyP["right_ud_wind_angle"] == 6) then keyP["right_ud_wind_angle"] = 62 elseif (keyP["right_ud_wind_angle"] == 7) then keyP["right_ud_wind_angle"] = 75 elseif (keyP["right_ud_wind_angle"] == 8) then keyP["right_ud_wind_angle"] = 88 elseif (keyP["right_ud_wind_angle"] == 9) then keyP["right_ud_wind_angle"] = 100 end
                    keyP["right_lr_wind_angle"] = bit.rshift(bit.band(messageBytes[cursor + 47], 0xF0), 4)
                    if (keyP["right_lr_wind_angle"] == 2) then keyP["right_lr_wind_angle"] = 13 elseif (keyP["right_lr_wind_angle"] == 3) then keyP["right_lr_wind_angle"] = 25 elseif (keyP["right_lr_wind_angle"] == 4) then keyP["right_lr_wind_angle"] = 38 elseif (keyP["right_lr_wind_angle"] == 5) then keyP["right_lr_wind_angle"] = 50 elseif (keyP["right_lr_wind_angle"] == 6) then keyP["right_lr_wind_angle"] = 62 elseif (keyP["right_lr_wind_angle"] == 7) then keyP["right_lr_wind_angle"] = 75 elseif (keyP["right_lr_wind_angle"] == 8) then keyP["right_lr_wind_angle"] = 88 elseif (keyP["right_lr_wind_angle"] == 9) then keyP["right_lr_wind_angle"] = 100 end
                end
                if (messageBytes[cursor + 3] > 44) then
                    keyP["linkage_2"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x08), 3)
                    keyP["quick_cool_heat"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x10), 4)
                    keyP["light"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x20), 5)
                    keyP["care_mode"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x40), 6)
                    keyP["care_mode_lock"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x80), 7)
                    keyP["screen_display_select"] = bit.rshift(bit.band(messageBytes[cursor + 48], 0x04), 2)
                    keyP["swing_lr_under_angle"] = bit.rshift(bit.band(messageBytes[cursor + 49], 0xF0), 4)
                    if (keyP["swing_lr_under_angle"] == 2) then keyP["swing_lr_under_angle"] = 13 elseif (keyP["swing_lr_under_angle"] == 3) then keyP["swing_lr_under_angle"] = 25 elseif (keyP["swing_lr_under_angle"] == 4) then keyP["swing_lr_under_angle"] = 38 elseif (keyP["swing_lr_under_angle"] == 5) then keyP["swing_lr_under_angle"] = 50 elseif (keyP["swing_lr_under_angle"] == 6) then keyP["swing_lr_under_angle"] = 62 elseif (keyP["swing_lr_under_angle"] == 7) then keyP["swing_lr_under_angle"] = 75 elseif (keyP["swing_lr_under_angle"] == 8) then keyP["swing_lr_under_angle"] = 88 elseif (keyP["swing_lr_under_angle"] == 9) then keyP["swing_lr_under_angle"] = 100 end
                end
                if (messageBytes[cursor + 3] > 46) then
                    keyP["circle_fan"] = bit.rshift(bit.band(messageBytes[cursor + 50], 0x08), 3)
                    keyP["circle_fan_mode"] = bit.band(messageBytes[cursor + 50], 0x07)
                    keyP["buzzer_off_status"] = bit.rshift(bit.band(messageBytes[cursor + 50], 0x10), 4)
                    keyP["buzzer_all"] = bit.rshift(bit.band(messageBytes[cursor + 50], 0x20), 5)
                    keyP["prevent_straight_wind_distance"] = bit.rshift(bit.band(messageBytes[cursor + 50], 0xC0), 6)
                end
                if (messageBytes[cursor + 3] > 47) then
                    keyP["linkage_2_temp_auto"] = bit.band(messageBytes[cursor + 51], 0x01)
                    keyP["linkage_2_wind_auto"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x02), 1)
                    keyP["linkage_2_fresh_air_auto"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x04), 2)
                    keyP["linkage_2_purifier_auto"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x08), 3)
                    keyP["linkage_2_humi_auto"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x10), 4)
                    keyP["air_remove_odor"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x40), 6)
                    keyP["auto_prevent_cold_wind_memory"] = bit.rshift(bit.band(messageBytes[cursor + 51], 0x80), 7)
                end
                if (messageBytes[cursor + 3] > 48) then keyP["eco_time_hour"] = messageBytes[cursor + 52] end
                if (messageBytes[cursor + 3] > 50) then
                    keyP["clean_breath"] = bit.rshift(bit.band(messageBytes[cursor + 54], 0x10), 4)
                    keyP["clean_breath_level"] = bit.rshift(bit.band(messageBytes[cursor + 54], 0x0E), 1)
                    keyP["health"] = bit.rshift(bit.band(messageBytes[cursor + 54], 0x40), 6)
                    keyP["humidification_mode"] = bit.rshift(bit.band(messageBytes[cursor + 54], 0x80), 7)
                end
                if (messageBytes[cursor + 3] > 52) then keyP["arofene_filter_use_time"] = messageBytes[cursor + 56] * 256 +
                    messageBytes[cursor + 55] end
                if (messageBytes[cursor + 3] > 53) then keyP["remove_odor_fan_speed"] = messageBytes[cursor + 57] end
                if (messageBytes[cursor + 3] > 54) then
                    keyP["humidification_fan_speed"] = bit.band(messageBytes[cursor + 58], 0x7F)
                    keyP["humidification"] = bit.rshift(bit.band(messageBytes[cursor + 58], 0x80), 7)
                end
                keyP["fresh_air"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x80), 7)
                keyP["voice_control_new"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x06), 1)
                keyP["voice_control"] = bit.rshift(bit.band(messageBytes[cursor + 22], 0x06), 1)
                keyP["ptc_default_rule"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0x20), 5)
                keyP["light_sensitive"] = bit.rshift(bit.band(messageBytes[cursor + 27], 0xC0), 6)
                keyP["wind_swing_ud_angle_up"] = messageBytes[cursor + 32]
                keyP["wind_swing_ud_angle_down"] = messageBytes[cursor + 33]
                keyP["wind_swing_lr_angle_up"] = messageBytes[cursor + 34]
                keyP["wind_swing_lr_angle_down"] = messageBytes[cursor + 35]
                keyP["analysis_value"] = keyP["analysis_value"] ..
                ",wind_swing_ud_angle_up,wind_swing_ud_angle_down,wind_swing_lr_angle_up,wind_swing_lr_angle_down"
                if (#binData >= 29) then
                    keyP["fresh_filter_time_total"] = messageBytes[cursor + 29] * 256 + messageBytes[cursor + 28]
                    keyP["fresh_filter_time_use"] = messageBytes[cursor + 31] * 256 + messageBytes[cursor + 30]
                    keyP["analysis_value"] = keyP["analysis_value"] ..
                    ",fresh_filter_time_total,fresh_filter_time_use,fresh_filter_timeout"
                end
                keyP["fresh_filter_time_use"] = messageBytes[cursor + 20] * 256 + messageBytes[cursor + 19]
                keyP["analysis_value"] = keyP["analysis_value"] .. ",fresh_filter_time_use"
                cursor = cursor + messageBytes[cursor + 3] + 4
            end
        end
    end
end
local function getTotalMsg(bodyData, cType)
    local bodyLength = #bodyData
    local msgLength = bodyLength + keyB["BYTE_PROTOCOL_LENGTH"] + 1
    local msgBytes = {}
    for i = 0, msgLength do msgBytes[i] = 0 end
    msgBytes[0] = keyB["BYTE_PROTOCOL_HEAD"]
    msgBytes[1] = bodyLength + keyB["BYTE_PROTOCOL_LENGTH"] + 1
    msgBytes[2] = keyB["BYTE_DEVICE_TYPE"]
    if (keyP["propertyNumber"] > 0) then msgBytes[8] = 0x02 end
    msgBytes[9] = cType
    for i = 0, bodyLength do msgBytes[i + keyB["BYTE_PROTOCOL_LENGTH"]] = bodyData[i] end
    msgBytes[msgLength] = makeSum(msgBytes, 1, msgLength - 1)
    local msgFinal = {}
    for i = 1, msgLength + 1 do msgFinal[i] = msgBytes[i - 1] end
    return msgFinal
end
function jsonToData(jsonCmd)
    if (#jsonCmd == 0) then return nil end
    local infoM = {}
    local bodyBytes = {}
    local json = decode(jsonCmd)
    deviceSubType = json["deviceinfo"]["deviceSubType"]
    local deviceSN = json["deviceinfo"]["deviceSN"]
    if deviceSN ~= nil then deviceSN8 = string.sub(deviceSN, 13, 17) end
    local query = json["query"]
    local control = json["control"]
    local status = json["status"]
    if (query) then
        local queryType = nil
        if (type(query) == "table") then queryType = query["query_type"] end
        if (queryType == nil) then queryType = "total_query" end
        if (queryType == "group_data_zero" or queryType == "group_data_four" or queryType == "group_data_one" or queryType == "group_data_five") then
            for i = 0, 21 do bodyBytes[i] = 0 end
            bodyBytes[0] = 0x41
            bodyBytes[1] = 0x21
            bodyBytes[2] = 0x01
            if (queryType == "group_data_zero") then bodyBytes[3] = 0x40 end
            if (queryType == "group_data_four") then bodyBytes[3] = 0x44 end
            if (queryType == "group_data_one") then bodyBytes[3] = 0x41 end
            if (queryType == "group_data_five") then bodyBytes[3] = 0x45 end
            math.randomseed(tostring(os.time() * #bodyBytes):reverse():sub(1, 7))
            math.random()
            bodyBytes[20] = math.random(1, 254)
            bodyBytes[21] = crc8_854(bodyBytes, 0, 20)
            infoM = getTotalMsg(bodyBytes, keyB["BYTE_QUERYL_REQUEST"])
        else
            bodyBytes[0] = 0xB1
            local propertyNum = 0
            local queryList = {}
            if (string.match(queryType, ",") == ",") then queryList = splitStrByChar(queryType, ",") else table.insert(
                queryList, queryType) end
            for v in values(queryList) do
                queryType = v
                if (queryType == "no_wind_sense") then
                    if (deviceSN8 == "12035" or deviceSN8 == "12037" or deviceSN8 == "Z1312" or deviceSN8 == "Z1262" or deviceSN8 == "12179" or deviceSN8 == "Z1261") then bodyBytes[1 + propertyNum * 2 + 1] = 0x43 else bodyBytes[1 + propertyNum * 2 + 1] = 0x18 end
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "fn_no_wind_sense") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x18
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "cool_hot_sense") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x21
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "nobody_energy_save") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x30
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "self_clean") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x39
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "child_prevent_cold_wind") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x3A
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "error_code_query") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x3F
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "mode_query") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x41
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "prevent_straight_wind") then
                    if (deviceSN8 == "12035" or deviceSN8 == "12037" or deviceSN8 == "Z1312" or deviceSN8 == "Z1262" or deviceSN8 == "12179" or deviceSN8 == "Z1261") then bodyBytes[1 + propertyNum * 2 + 1] = 0x43 else bodyBytes[1 + propertyNum * 2 + 1] = 0x42 end
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "gentle_wind_sense") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x86
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "fa_prevent_straight_wind") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x43
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "prevent_super_cool") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x49
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "high_temperature_monitor") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x47
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "rate_select") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x48
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "intelligent_wind") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x34
                    if (deviceSN8 == "50939" or deviceSN8 == "51001" or deviceSN8 == "Z1304" or deviceSN8 == "Z1259" or deviceSN8 == "Z2272") then bodyBytes[1 + propertyNum * 2 + 1] = 0x33 end
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_straight" or queryType == "yb_wind_avoid") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x32
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_avoid") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x33
                    if (deviceSN8 == "50939" or deviceSN8 == "51001" or deviceSN8 == "Z1304" or deviceSN8 == "Z1259" or deviceSN8 == "Z2272") then bodyBytes[1 + propertyNum * 2 + 1] = 0x32 end
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "auto_prevent_straight_wind") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x26
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "security") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x29
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "even_wind") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x4E
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "single_tuyere") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x4F
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "extreme_wind") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x4C
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "voice_control") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x20
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "pre_cool_hot") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x01
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "water_washing") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x4A
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "fresh_air") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x4B
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "parent_control") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x51
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "filter_value") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x09
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x04
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_swing_ud_angle") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x09
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_swing_lr_angle") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x0A
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "prevent_straight_wind_lr") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x58
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "pm25_value") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x0B
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "water_pump") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x50
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "intelligent_control") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x31
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "volume_control") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x24
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "voice_control_new") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x20
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "face_register") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x44
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "cool_temp_down" or queryType == "cool_temp_up" or queryType == "auto_temp_down" or queryType == "auto_temp_up" or queryType == "heat_temp_down" or queryType == "heat_temp_up") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x25
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "remote_control_lock") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x27
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "operating_time") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x28
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "indoor_humidity") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x15
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "degerming") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x5A
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "light") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x5B
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "care_mode") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xB5
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "care_mode_lock") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xB6
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_around") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x59
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_top") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x61
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "child_lock") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x5C
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "buzzer_all") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x2C
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "self_remove_odor_phase") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x5D
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "high_temp_remove_odor_alone") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x5E
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "power_lock") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x27
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "ptc_lock") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x29
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "offline_operating_time") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x2B
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "ozone") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x5F
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "soft_warm") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x63
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "fresh_air_parm") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x50
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "rewarming_dry") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x68
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "arom") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x69
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "new_mode_power") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x01
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "uvc_remove_odor") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x6F
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "whirl_wind_left" or queryType == "whirl_wind_right") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x71
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "inner_purifier") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x70
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "light_sensitive") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x08
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "indoor_co2") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x73
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "remove_odor") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x77
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "fresh_air_on_co2") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x76
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "jet_cool") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x67
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "main_horizontal_guide_strip_1" or queryType == "main_horizontal_guide_strip_2" or queryType == "main_horizontal_guide_strip_3" or queryType == "main_horizontal_guide_strip_4") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x30
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "linkage") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x7B
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "moisturizing") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x7C
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "no_wind_sense_left" or queryType == "no_wind_sense_right") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x74
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "power") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x7F
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "mode") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x02
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "temperature") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x03
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_speed") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x06
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "total_query") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x7E
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_swing_lr" or queryType == "wind_swing_lr_left") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x80
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_swing_lr_right") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x81
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_swing_ud" or queryType == "wind_swing_ud_left") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x82
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_swing_ud_right") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x83
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_speed_right") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x84
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "dry") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x10
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "power_on_timer") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x0B
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "power_off_timer") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x0C
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "screen_display") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x17
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "ptc") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x0F
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "ptc_default_rule") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x11
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "fresh_filter_reset") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x85
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "eco") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x0D
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "comfort_sleep") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x11
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "comfort_power_save") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x22
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "screen_display_time") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x87
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wait_clean") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x99
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "ptc_load") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xA0
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "self_clean_time" or queryType == "self_clean_stage") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x9A
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "dry_clean_time" or queryType == "dry_clean_stage") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x9B
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "no_wind_sense_judge_param") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x9F
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "left_down_real_wind_speed") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x07
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "right_up_real_wind_speed") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xA4
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "left_ud_wind_angle") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x09
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "up_lr_wind_angle") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x0A
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "swing_lr_under_angle") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x96
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "right_ud_wind_angle") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xA1
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "left_lr_wind_angle") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xA1
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "right_lr_wind_angle") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xA1
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "defrosting_load") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xA8
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "e2_query") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xE2
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "e0_query") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xE0
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_swing_ud_angle_up" or queryType == "wind_swing_ud_angle_down" or queryType == "app_control_remember_ud") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x79
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_swing_lr_angle_up" or queryType == "wind_swing_lr_angle_down" or queryType == "app_control_remember_lr") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x7A
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "smart_dry_value") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x14
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "screen_display_select") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x36
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "wind_swing_lr_under") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xAE
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "no_wind_sense_up" or queryType == "no_wind_sense_down") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xAF
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "auto_prevent_cold_wind") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x78
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "linkage_2") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xB2
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "quick_cool_heat") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xB3
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "cool_power_saving") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x89
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "ieco_switch") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xE3
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "prepare_food") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x54
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "quick_fry") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x55
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "light_color_control") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xB7
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "quick_fry_center_point" or queryType == "quick_fry_angle") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x8B
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "circle_fan") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xB9
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "power_saving") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x62
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "prevent_straight_wind_distance") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x38
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "auto_prevent_cold_wind_memory") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xBC
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "buzzer_off_status") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x2F
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x02
                    propertyNum = propertyNum + 1
                end
                if (queryType == "air_remove_odor") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xBF
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "clean_breath") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xC7
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "remove_arofene_clean") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xC8
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "health") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xC9
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "strong_cool") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0xCA
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
                if (queryType == "humidification") then
                    bodyBytes[1 + propertyNum * 2 + 1] = 0x75
                    bodyBytes[1 + propertyNum * 2 + 2] = 0x00
                    propertyNum = propertyNum + 1
                end
            end
            bodyBytes[1] = propertyNum
            math.randomseed(tostring(os.time() * #bodyBytes):reverse():sub(1, 7))
            math.random()
            bodyBytes[1 + propertyNum * 2 + 1] = math.random(1, 254)
            bodyBytes[1 + propertyNum * 2 + 2] = crc8_854(bodyBytes, 0, 1 + propertyNum * 2 + 1)
            infoM = getTotalMsg(bodyBytes, keyB["BYTE_QUERYL_REQUEST"])
        end
    elseif (control) then
        if (status) then jsonToModel(status, "status") end
        keyP["ieco_status"] = 0
        if (control) then
            if (control["ilinkId"] ~= nil and control["ticket"] ~= nil) then
                local short_length = 4 + #control["ilinkId"] + #control["ticket"]
                local length = short_length + 12
                local count = 0
                for i = 0, length + 1 do bodyBytes[i] = 0 end
                bodyBytes[0] = 0xAA
                bodyBytes[1] = length
                bodyBytes[2] = 0xAC
                bodyBytes[3] = 0x00
                bodyBytes[8] = 0x02
                bodyBytes[9] = 0x91
                bodyBytes[10] = 0xAC
                bodyBytes[11] = 0x0B
                bodyBytes[12] = short_length
                bodyBytes[14] = #control["ilinkId"]
                bodyBytes[15] = #control["ticket"]
                for i = 0, #control["ilinkId"] - 1 do
                    bodyBytes[16 + i] = string.byte(string.sub(control["ilinkId"], i + 1, i + 1))
                    count = count + 1
                end
                for i = 0, #control["ticket"] - 1 do bodyBytes[16 + count + i] = string.byte(string.sub(
                    control["ticket"], i + 1, i + 1)) end
                bodyBytes[length] = makeSum(bodyBytes, 1, length - 1)
                local ret = table2string2(bodyBytes)
                ret = string2hexstring(ret)
                return ret
            end
            jsonToModel(control, "control")
        end
        if (keyP["propertyNumber"] == 0) then else
            bodyBytes[0] = keyB["BYTE_CONTROL_PROPERTY_CMD"]
            bodyBytes[1] = keyP["propertyNumber"]
            local cursor = 2
            if (keyP["prevent_super_cool"] ~= nil) then
                bodyBytes[cursor + 0] = 0x49
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x05
                bodyBytes[cursor + 3] = keyP["prevent_super_cool"]
                bodyBytes[cursor + 4] = 0xFF
                bodyBytes[cursor + 5] = 0xFF
                bodyBytes[cursor + 6] = 0xFF
                bodyBytes[cursor + 7] = 0xFF
                cursor = cursor + 8
            end
            if (keyP["prevent_straight_wind"] ~= nil) then if (deviceSN8 == "12035" or deviceSN8 == "12037" or deviceSN8 == "Z1312" or deviceSN8 == "Z1262" or deviceSN8 == "12179" or deviceSN8 == "Z1261") then
                    bodyBytes[cursor + 0] = 0x43
                    bodyBytes[cursor + 1] = 0x00
                    bodyBytes[cursor + 2] = 0x01
                    bodyBytes[cursor + 3] = 0x00
                    if (keyP["prevent_straight_wind"] == 2) then bodyBytes[cursor + 3] = 0x02 elseif (keyP["prevent_straight_wind"] == 1) then bodyBytes[cursor + 3] = 0x01 end
                    cursor = cursor + 4
                else
                    bodyBytes[cursor + 0] = 0x42
                    bodyBytes[cursor + 1] = 0x00
                    bodyBytes[cursor + 2] = 0x01
                    bodyBytes[cursor + 3] = keyP["prevent_straight_wind"]
                    cursor = cursor + 4
                end end
            if (keyP["fa_prevent_straight_wind"] ~= nil) then
                bodyBytes[cursor + 0] = 0x43
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = 0x00
                if (keyP["fa_prevent_straight_wind"] == 2) then bodyBytes[cursor + 3] = 0x02 elseif (keyP["fa_prevent_straight_wind"] == 1) then bodyBytes[cursor + 3] = 0x01 end
                cursor = cursor + 4
            end
            if (keyP["auto_prevent_straight_wind"] ~= nil) then
                bodyBytes[cursor + 0] = 0x26
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["auto_prevent_straight_wind"]
                cursor = cursor + 4
            end
            if (keyP["self_clean"] ~= nil) then
                bodyBytes[cursor + 0] = 0x39
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["self_clean"]
                cursor = cursor + 4
            end
            if (keyP["wind_straight"] ~= nil) then
                bodyBytes[cursor + 0] = 0x32
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["wind_straight"]
                cursor = cursor + 4
            end
            if (keyP["yb_wind_avoid"] ~= nil) then
                bodyBytes[cursor + 0] = 0x32
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["yb_wind_avoid"]
                cursor = cursor + 4
            end
            if (keyP["wind_avoid"] ~= nil) then if (deviceSN8 == "50939" or deviceSN8 == "51001" or deviceSN8 == "Z1304" or deviceSN8 == "Z1259" or deviceSN8 == "Z2272") then
                    bodyBytes[cursor + 0] = 0x32
                    bodyBytes[cursor + 1] = 0x00
                    bodyBytes[cursor + 2] = 0x01
                    if (keyP["wind_avoid"] == 0x01) then bodyBytes[cursor + 3] = 0x02 else bodyBytes[cursor + 3] = 0x00 end
                    cursor = cursor + 4
                else
                    bodyBytes[cursor + 0] = 0x33
                    bodyBytes[cursor + 1] = 0x00
                    bodyBytes[cursor + 2] = 0x01
                    bodyBytes[cursor + 3] = keyP["wind_avoid"]
                    cursor = cursor + 4
                end end
            if (keyP["intelligent_wind"] ~= nil) then
                bodyBytes[cursor + 0] = 0x34
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["intelligent_wind"]
                cursor = cursor + 4
            end
            if (keyP["no_wind_sense"] ~= nil) then
                bodyBytes[cursor + 0] = 0x18
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["no_wind_sense"]
                cursor = cursor + 4
            end
            if (keyP["child_prevent_cold_wind"] ~= nil) then
                bodyBytes[cursor + 0] = 0x3A
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["child_prevent_cold_wind"]
                cursor = cursor + 4
            end
            if (keyP["little_angel"] ~= nil) then
                bodyBytes[cursor + 0] = 0x1B
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["little_angel"]
                cursor = cursor + 4
            end
            if (keyP["cool_hot_sense"] ~= nil) then
                bodyBytes[cursor + 0] = 0x21
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x08
                bodyBytes[cursor + 3] = keyP["cool_hot_sense"]
                bodyBytes[cursor + 4] = 0x00
                bodyBytes[cursor + 5] = 0x00
                bodyBytes[cursor + 6] = 0x00
                bodyBytes[cursor + 7] = 0x00
                bodyBytes[cursor + 8] = 0x00
                bodyBytes[cursor + 9] = 0x00
                bodyBytes[cursor + 10] = 0x00
                cursor = cursor + 11
            end
            if (keyP["gentle_wind_sense"] ~= nil) then
                bodyBytes[cursor + 0] = 0x86
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["gentle_wind_sense"]
                cursor = cursor + 4
            end
            if (keyP["even_wind"] ~= nil) then
                bodyBytes[cursor + 0] = 0x4E
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["even_wind"]
                cursor = cursor + 4
            end
            if (keyP["single_tuyere"] ~= nil) then
                bodyBytes[cursor + 0] = 0x4F
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["single_tuyere"]
                cursor = cursor + 4
            end
            if (keyP["extreme_wind"] ~= nil) then
                bodyBytes[cursor + 0] = 0x4C
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["extreme_wind"]
                bodyBytes[cursor + 4] = 0x01
                cursor = cursor + 5
            end
            if (keyP["security"] ~= nil) then
                bodyBytes[cursor + 0] = 0x29
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["security"]
                cursor = cursor + 4
            end
            if (keyP["voice_control"] ~= nil) then
                bodyBytes[cursor + 0] = 0x20
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x09
                bodyBytes[cursor + 3] = keyP["voice_control"]
                bodyBytes[cursor + 4] = 0xFF
                bodyBytes[cursor + 5] = 0xFF
                bodyBytes[cursor + 6] = 0xFF
                bodyBytes[cursor + 7] = 0xFF
                bodyBytes[cursor + 8] = 0xFF
                bodyBytes[cursor + 9] = 0xFF
                bodyBytes[cursor + 10] = 0xFF
                bodyBytes[cursor + 11] = 0xFF
                cursor = cursor + 12
            end
            if (keyP["pre_cool_hot"] ~= nil) then
                bodyBytes[cursor + 0] = 0x01
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["pre_cool_hot"]
                cursor = cursor + 4
            end
            if (keyP["water_washing"] ~= nil) then
                bodyBytes[cursor + 0] = 0x4A
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x04
                bodyBytes[cursor + 3] = keyP["water_washing_manual"]
                bodyBytes[cursor + 4] = keyP["water_washing"]
                bodyBytes[cursor + 5] = keyP["water_washing_time"]
                bodyBytes[cursor + 6] = 0xFF
                cursor = cursor + 7
            end
            if (keyP["fresh_air"] ~= nil) then
                bodyBytes[cursor + 0] = 0x4B
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x04
                bodyBytes[cursor + 3] = keyP["fresh_air"]
                bodyBytes[cursor + 4] = keyP["fresh_air_fan_speed"]
                bodyBytes[cursor + 5] = 0xFF
                bodyBytes[cursor + 6] = keyP["fresh_air_mode_two"]
                cursor = cursor + 7
            end
            if (keyP["parent_control"] ~= nil) then
                bodyBytes[cursor + 0] = 0x51
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x05
                bodyBytes[cursor + 3] = keyP["parent_control"]
                bodyBytes[cursor + 4] = keyP["parent_control_temp_up"]
                bodyBytes[cursor + 5] = keyP["parent_control_temp_down"]
                bodyBytes[cursor + 6] = 0xFF
                bodyBytes[cursor + 7] = 0xFF
                cursor = cursor + 8
            end
            if (keyP["buzzerValue"] ~= nil) then
                bodyBytes[cursor + 0] = 0x1A
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = 0x00
                if (keyP["buzzerValue"] == 0x40) then bodyBytes[cursor + 3] = 0x01 end
                cursor = cursor + 4
                bodyBytes[1] = keyP["propertyNumber"] + 1
            end
            if (keyP["wind_swing_ud_angle"] ~= nil or keyP["left_ud_wind_angle"] ~= nil) then
                bodyBytes[cursor + 0] = 0x09
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                if (keyP["wind_swing_ud_angle"] ~= nil) then bodyBytes[cursor + 3] = keyP["wind_swing_ud_angle"] end
                if (keyP["left_ud_wind_angle"] ~= nil) then bodyBytes[cursor + 3] = keyP["left_ud_wind_angle"] end
                cursor = cursor + 4
            end
            if (keyP["wind_swing_lr_angle"] ~= nil) then
                bodyBytes[cursor + 0] = 0x0A
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["wind_swing_lr_angle"]
                cursor = cursor + 4
            end
            if (keyP["nobody_energy_save"] ~= nil) then
                bodyBytes[cursor + 0] = 0x30
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x06
                bodyBytes[cursor + 3] = keyP["nobody_energy_save"]
                bodyBytes[cursor + 4] = 0x00
                bodyBytes[cursor + 5] = 0x00
                bodyBytes[cursor + 6] = 0x00
                bodyBytes[cursor + 7] = 0x00
                bodyBytes[cursor + 8] = 0x00
                cursor = cursor + 9
                bodyBytes[1] = keyP["propertyNumber"] + 1
            end
            if (keyP["prevent_straight_wind_lr"] ~= nil) then
                bodyBytes[cursor + 0] = 0x58
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["prevent_straight_wind_lr"]
                cursor = cursor + 4
                bodyBytes[1] = keyP["propertyNumber"] + 1
            end
            if (keyP["water_pump"] ~= nil) then
                bodyBytes[cursor + 0] = 0x50
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["water_pump"]
                cursor = cursor + 4
                bodyBytes[1] = keyP["propertyNumber"] + 1
            end
            if (keyP["intelligent_control"] ~= nil) then
                bodyBytes[cursor + 0] = 0x31
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["intelligent_control"]
                cursor = cursor + 4
                bodyBytes[1] = keyP["propertyNumber"] + 1
            end
            if (keyP["volume_control"] ~= nil) then
                bodyBytes[cursor + 0] = 0x24
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x04
                bodyBytes[cursor + 3] = 0x02
                bodyBytes[cursor + 4] = keyP["volume_control"]
                bodyBytes[cursor + 5] = 0xFF
                bodyBytes[cursor + 6] = 0xFF
                cursor = cursor + 7
                bodyBytes[1] = keyP["propertyNumber"] + 1
            end
            if (keyP["voice_control_new"] ~= nil) then
                bodyBytes[cursor + 0] = 0x20
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x14
                bodyBytes[cursor + 3] = keyP["voice_control_new"]
                bodyBytes[cursor + 4] = 0xFF
                bodyBytes[cursor + 5] = 0xFF
                bodyBytes[cursor + 6] = 0xFF
                bodyBytes[cursor + 7] = 0xFF
                bodyBytes[cursor + 8] = 0xFF
                bodyBytes[cursor + 9] = 0xFF
                bodyBytes[cursor + 10] = 0xFF
                bodyBytes[cursor + 11] = 0xFF
                bodyBytes[cursor + 12] = 0xFF
                bodyBytes[cursor + 13] = 0xFF
                bodyBytes[cursor + 14] = 0xFF
                bodyBytes[cursor + 15] = 0xFF
                bodyBytes[cursor + 16] = 0xFF
                bodyBytes[cursor + 17] = 0xFF
                bodyBytes[cursor + 18] = 0xFF
                bodyBytes[cursor + 19] = 0xFF
                bodyBytes[cursor + 20] = 0xFF
                bodyBytes[cursor + 21] = 0xFF
                bodyBytes[cursor + 22] = 0xFF
                cursor = cursor + 23
            end
            if (keyP["cool_temp_down"] ~= nil or keyP["cool_temp_up"] ~= nil or keyP["auto_temp_down"] ~= nil or keyP["auto_temp_up"] ~= nil or keyP["heat_temp_down"] ~= nil or keyP["heat_temp_up"] ~= nil) then
                bodyBytes[cursor + 0] = 0x25
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x07
                bodyBytes[cursor + 3] = keyP["cool_temp_down"]
                bodyBytes[cursor + 4] = keyP["cool_temp_up"]
                bodyBytes[cursor + 5] = keyP["auto_temp_down"]
                bodyBytes[cursor + 6] = keyP["auto_temp_up"]
                bodyBytes[cursor + 7] = keyP["heat_temp_down"]
                bodyBytes[cursor + 8] = keyP["heat_temp_up"]
                bodyBytes[cursor + 9] = 0x00
                cursor = cursor + 10
            end
            if (keyP["remote_control_lock"] ~= nil) then
                bodyBytes[cursor + 0] = 0x27
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["remote_control_lock"]
                bodyBytes[cursor + 4] = keyP["remote_control_lock_control"]
                cursor = cursor + 5
            end
            if (keyP["operating_time"] ~= nil) then
                bodyBytes[cursor + 0] = 0x28
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x03
                bodyBytes[cursor + 3] = bit.band(keyP["operating_time"], 0xff)
                bodyBytes[cursor + 4] = bit.band(bit.rshift(keyP["operating_time"], 8), 0xff)
                bodyBytes[cursor + 5] = bit.band(bit.rshift(keyP["operating_time"], 16), 0xff)
                cursor = cursor + 6
            end
            if (keyP["degerming"] ~= nil) then
                bodyBytes[cursor + 0] = 0x5A
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["degerming"]
                cursor = cursor + 4
                bodyBytes[1] = keyP["propertyNumber"] + 1
            end
            if (keyP["light"] ~= nil) then
                bodyBytes[cursor + 0] = 0x5B
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["light"]
                cursor = cursor + 4
            end
            if (keyP["care_mode"] ~= nil) then
                bodyBytes[cursor + 0] = 0xB5
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["care_mode"]
                cursor = cursor + 4
            end
            if (keyP["care_mode_lock"] ~= nil) then
                bodyBytes[cursor + 0] = 0xB6
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["care_mode_lock"]
                cursor = cursor + 4
            end
            if (keyP["wind_top"] ~= nil) then
                bodyBytes[cursor + 0] = 0x61
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["wind_top"]
                cursor = cursor + 4
            end
            if (keyP["child_lock"] ~= nil) then
                bodyBytes[cursor + 0] = 0x5C
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["child_lock"]
                cursor = cursor + 4
            end
            if (keyP["buzzer_all"] ~= nil) then
                bodyBytes[cursor + 0] = 0x2C
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["buzzer_all"]
                cursor = cursor + 4
            end
            if (keyP["wind_around"] ~= nil) then
                bodyBytes[cursor + 0] = 0x59
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["wind_around"]
                bodyBytes[cursor + 4] = 0
                if (keyP["wind_around_ud"] ~= nil) then bodyBytes[cursor + 4] = keyP["wind_around_ud"] end
                cursor = cursor + 5
            end
            if (keyP["self_remove_odor_phase"] ~= nil) then
                bodyBytes[cursor + 0] = 0x5D
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["self_remove_odor_phase"]
                cursor = cursor + 4
            end
            if (keyP["high_temp_remove_odor_alone"] ~= nil) then
                bodyBytes[cursor + 0] = 0x5E
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["high_temp_remove_odor_alone"]
                cursor = cursor + 4
            end
            if (keyP["power_lock"] ~= nil) then
                bodyBytes[cursor + 0] = 0x27
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["power_lock"]
                cursor = cursor + 4
            end
            if (keyP["ptc_lock"] ~= nil) then
                bodyBytes[cursor + 0] = 0x29
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["ptc_lock"]
                cursor = cursor + 4
            end
            if (keyP["offline_operating_time"] ~= nil) then
                bodyBytes[cursor + 0] = 0x2B
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = bit.band(keyP["offline_operating_time"], 0xff)
                bodyBytes[cursor + 4] = bit.band(bit.rshift(keyP["offline_operating_time"], 8), 0xff)
                cursor = cursor + 5
            end
            if (keyP["ozone"] ~= nil) then
                bodyBytes[cursor + 0] = 0x5F
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["ozone"]
                cursor = cursor + 4
            end
            if (keyP["soft_warm"] ~= nil) then
                bodyBytes[cursor + 0] = 0x63
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["soft_warm"]
                cursor = cursor + 4
            end
            if (keyP["fresh_air_parm"] ~= nil) then
                bodyBytes[cursor + 0] = 0x50
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["fresh_air_parm"]
                cursor = cursor + 4
            end
            if (keyP["rewarming_dry"] ~= nil) then
                bodyBytes[cursor + 0] = 0x68
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["rewarming_dry"]
                cursor = cursor + 4
            end
            if (keyP["arom"] ~= nil) then
                bodyBytes[cursor + 0] = 0x69
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x07
                bodyBytes[cursor + 3] = keyP["arom"]
                bodyBytes[cursor + 4] = keyP["arom_fan_speed"]
                bodyBytes[cursor + 5] = keyP["arom_time_clean"]
                bodyBytes[cursor + 6] = bit.band(keyP["arom_time"], 0xff)
                bodyBytes[cursor + 7] = bit.band(bit.rshift(keyP["arom_time"], 8), 0xff)
                bodyBytes[cursor + 8] = bit.band(keyP["arom_time_total"], 0xff)
                bodyBytes[cursor + 9] = bit.band(bit.rshift(keyP["arom_time_total"], 8), 0xff)
                cursor = cursor + 10
            end
            if (keyP["new_mode_power"] ~= nil) then
                bodyBytes[cursor + 0] = 0x01
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x04
                bodyBytes[cursor + 3] = keyP["new_mode_power"]
                bodyBytes[cursor + 4] = keyP["new_mode"]
                bodyBytes[cursor + 5] = keyP["new_temperature"]
                bodyBytes[cursor + 6] = keyP["new_wind_speed"]
                cursor = cursor + 7
            end
            if (keyP["uvc_remove_odor"] ~= nil) then
                bodyBytes[cursor + 0] = 0x6F
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["uvc_remove_odor"]
                bodyBytes[cursor + 4] = keyP["uvc_power_off"]
                cursor = cursor + 5
            end
            if (keyP["main_strip_control"] ~= nil) then
                bodyBytes[cursor + 0] = 0x30
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x04
                bodyBytes[cursor + 3] = keyP["main_horizontal_guide_strip_1"]
                bodyBytes[cursor + 4] = keyP["main_horizontal_guide_strip_2"]
                bodyBytes[cursor + 5] = keyP["main_horizontal_guide_strip_3"]
                bodyBytes[cursor + 6] = keyP["main_horizontal_guide_strip_4"]
                cursor = cursor + 7
            end
            if (keyP["light_sensitive"] ~= nil) then
                bodyBytes[cursor + 0] = 0x08
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["light_sensitive"]
                cursor = cursor + 4
            end
            if (keyP["ieco_status"] == 1) then
                bodyBytes[cursor + 0] = 0xE3
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x10
                bodyBytes[cursor + 3] = keyP["ieco_frame"]
                bodyBytes[cursor + 4] = keyP["ieco_number"]
                bodyBytes[cursor + 5] = keyP["ieco_switch"]
                bodyBytes[cursor + 6] = bit.band(keyP["ieco_target_rate"], 0xff)
                bodyBytes[cursor + 7] = bit.band(bit.rshift(keyP["ieco_target_rate"], 8), 0xff)
                bodyBytes[cursor + 8] = keyP["ieco_indoor_wind_speed_level"]
                bodyBytes[cursor + 9] = bit.band(keyP["ieco_indoor_wind_speed"], 0xff)
                bodyBytes[cursor + 10] = bit.band(bit.rshift(keyP["ieco_indoor_wind_speed"], 8), 0xff)
                bodyBytes[cursor + 11] = keyP["ieco_outdoor_wind_speed_level"]
                bodyBytes[cursor + 12] = bit.band(keyP["ieco_outdoor_wind_speed"], 0xff)
                bodyBytes[cursor + 13] = bit.band(bit.rshift(keyP["ieco_outdoor_wind_speed"], 8), 0xff)
                bodyBytes[cursor + 14] = bit.band(keyP["ieco_expansion_valve"], 0xff)
                bodyBytes[cursor + 15] = bit.band(bit.rshift(keyP["ieco_expansion_valve"], 8), 0xff)
                bodyBytes[cursor + 16] = keyP["dynamic_temp_compensation"]
                bodyBytes[cursor + 17] = bit.band((keyP["frequency_compensation"]) * 100 + 65535 + 1, 0xff)
                bodyBytes[cursor + 18] = bit.rshift(bit.band((keyP["frequency_compensation"]) * 100 + 65535 + 1, 0xff00),
                    8)
                cursor = cursor + 19
            end
            if ((keyP["whirl_wind_left"] ~= nil or keyP["whirl_wind_right"] ~= nil) and tempControl == 1) then
                bodyBytes[cursor + 0] = 0x71
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["whirl_wind_left"]
                bodyBytes[cursor + 4] = keyP["whirl_wind_right"]
                cursor = cursor + 5
            end
            if (keyP["inner_purifier"] ~= nil) then
                bodyBytes[cursor + 0] = 0x70
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x03
                bodyBytes[cursor + 3] = keyP["inner_purifier"]
                bodyBytes[cursor + 4] = keyP["inner_purifier_fan_speed"]
                bodyBytes[cursor + 5] = keyP["inner_purifier_mode"]
                cursor = cursor + 6
            end
            if (keyP["remove_odor"] ~= nil) then
                bodyBytes[cursor + 0] = 0x77
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["remove_odor"]
                bodyBytes[cursor + 4] = keyP["remove_odor_fan_speed"]
                cursor = cursor + 5
            end
            if (keyP["fresh_air_on_co2"] ~= nil or keyP["fresh_air_off_co2"] ~= nil) then
                bodyBytes[cursor + 0] = 0x76
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x04
                bodyBytes[cursor + 3] = bit.band(keyP["fresh_air_on_co2"], 0xff)
                bodyBytes[cursor + 4] = bit.band(bit.rshift(keyP["fresh_air_on_co2"], 8), 0xff)
                bodyBytes[cursor + 5] = bit.band(keyP["fresh_air_off_co2"], 0xff)
                bodyBytes[cursor + 6] = bit.band(bit.rshift(keyP["fresh_air_off_co2"], 8), 0xff)
                cursor = cursor + 7
            end
            if (keyP["linkage"] ~= nil) then
                bodyBytes[cursor + 0] = 0x7B
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["linkage"]
                cursor = cursor + 4
            end
            if (keyP["moisturizing"] ~= nil) then
                bodyBytes[cursor + 0] = 0x7C
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["moisturizing"]
                bodyBytes[cursor + 4] = keyP["moisturizing_fan_speed"]
                cursor = cursor + 5
            end
            if (keyP["no_wind_sense_control"] ~= nil) then
                bodyBytes[cursor + 0] = 0x74
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["no_wind_sense_left"]
                bodyBytes[cursor + 4] = keyP["no_wind_sense_right"]
                cursor = cursor + 5
            end
            if (keyP["powerValue"] ~= nil) then
                bodyBytes[cursor + 0] = 0x7F
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["powerValue"]
                cursor = cursor + 4
            end
            if (keyP["modeValue"] ~= nil) then
                bodyBytes[cursor + 0] = 0x02
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["modeValue"]
                cursor = cursor + 4
            end
            if (keyP["fanspeedValue"] ~= nil) then
                bodyBytes[cursor + 0] = 0x06
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["fanspeedValue"]
                cursor = cursor + 4
            end
            if (keyP["temperature"] ~= nil) then
                bodyBytes[cursor + 0] = 0x03
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = (keyP["temperature"] + keyP["smallTemperature"]) * 2 + 50
                cursor = cursor + 4
            end
            if (keyP["swingLRValue"] ~= nil or keyP["wind_swing_lr_left"] ~= nil) then
                bodyBytes[cursor + 0] = 0x80
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                if (keyP["swingLRValue"] ~= nil) then bodyBytes[cursor + 3] = keyP["swingLRValue"] end
                if (keyP["wind_swing_lr_left"] ~= nil) then bodyBytes[cursor + 3] = keyP["wind_swing_lr_left"] end
                cursor = cursor + 4
            end
            if (keyP["wind_swing_lr_right"] ~= nil) then
                bodyBytes[cursor + 0] = 0x81
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["wind_swing_lr_right"]
                cursor = cursor + 4
            end
            if (keyP["swingUDValue"] ~= nil or keyP["wind_swing_ud_left"] ~= nil) then
                bodyBytes[cursor + 0] = 0x82
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                if (keyP["swingUDValue"] ~= nil) then bodyBytes[cursor + 3] = keyP["swingUDValue"] end
                if (keyP["wind_swing_ud_left"] ~= nil) then bodyBytes[cursor + 3] = keyP["wind_swing_ud_left"] end
                cursor = cursor + 4
            end
            if (keyP["wind_swing_ud_right"] ~= nil) then
                bodyBytes[cursor + 0] = 0x83
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["wind_swing_ud_right"]
                cursor = cursor + 4
            end
            if (keyP["wind_speed_right"] ~= nil) then
                bodyBytes[cursor + 0] = 0x84
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["wind_speed_right"]
                cursor = cursor + 4
            end
            if (keyP["dryValue"] ~= nil) then
                bodyBytes[cursor + 0] = 0x10
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["dryValue"]
                cursor = cursor + 4
            end
            if (keyP["openTimerSwitch"] ~= nil) then
                bodyBytes[cursor + 0] = 0x0B
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x03
                bodyBytes[cursor + 3] = keyP["openTimerSwitch"]
                bodyBytes[cursor + 4] = keyP["openHour"]
                bodyBytes[cursor + 5] = keyP["openStepMintues"]
                cursor = cursor + 6
            end
            if (keyP["closeTimerSwitch"] ~= nil) then
                bodyBytes[cursor + 0] = 0x0C
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x03
                bodyBytes[cursor + 3] = keyP["closeTimerSwitch"]
                bodyBytes[cursor + 4] = keyP["closeHour"]
                bodyBytes[cursor + 5] = keyP["closeStepMintues"]
                cursor = cursor + 6
            end
            if (keyP["screen_display"] ~= nil) then
                bodyBytes[cursor + 0] = 0x17
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["screen_display"]
                cursor = cursor + 4
            end
            if (keyP["PTCValue"] ~= nil) then
                bodyBytes[cursor + 0] = 0x0F
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["PTCValue"]
                cursor = cursor + 4
            end
            if (keyP["ptc_default_rule"] ~= nil) then
                bodyBytes[cursor + 0] = 0x11
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["ptc_default_rule"]
                cursor = cursor + 4
            end
            if (keyP["fresh_filter_reset"] ~= nil) then
                bodyBytes[cursor + 0] = 0x85
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["fresh_filter_reset"]
                cursor = cursor + 4
            end
            if (keyP["ecoValue"] ~= nil) then
                bodyBytes[cursor + 0] = 0x0D
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["ecoValue"]
                cursor = cursor + 4
            end
            if (keyP["comfortableSleepValue"] ~= nil) then
                bodyBytes[cursor + 0] = 0x11
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x0C
                bodyBytes[cursor + 3] = keyP["comfortableSleepValue"]
                bodyBytes[cursor + 4] = keyP["comfortableSleepTime"]
                bodyBytes[cursor + 5] = comfortByte[1] * 2
                bodyBytes[cursor + 6] = comfortByte[2] * 2
                bodyBytes[cursor + 7] = comfortByte[3] * 2
                bodyBytes[cursor + 8] = comfortByte[4] * 2
                bodyBytes[cursor + 9] = comfortByte[5] * 2
                bodyBytes[cursor + 10] = comfortByte[6] * 2
                bodyBytes[cursor + 11] = comfortByte[7] * 2
                bodyBytes[cursor + 12] = comfortByte[8] * 2
                bodyBytes[cursor + 13] = comfortByte[9] * 2
                bodyBytes[cursor + 14] = comfortByte[10] * 2
                cursor = cursor + 15
            end
            if (keyP["comfortPowerSave"] ~= nil) then
                bodyBytes[cursor + 0] = 0x22
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["comfortPowerSave"]
                cursor = cursor + 4
            end
            if (keyP["screen_display_time"] ~= nil) then
                bodyBytes[cursor + 0] = 0x87
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["screen_display_time"]
                cursor = cursor + 4
            end
            if (keyP["total_status_switch"] ~= nil) then
                bodyBytes[cursor + 0] = 0x88
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["total_status_switch"]
                cursor = cursor + 4
            end
            if (keyP["wait_clean"] ~= nil) then
                bodyBytes[cursor + 0] = 0x99
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["wait_clean"]
                cursor = cursor + 4
            end
            if (keyP["self_clean_time"] ~= nil) then
                bodyBytes[cursor + 0] = 0x9A
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["self_clean_time"]
                cursor = cursor + 4
            end
            if (keyP["dry_clean_time"] ~= nil) then
                bodyBytes[cursor + 0] = 0x9B
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["dry_clean_time"]
                cursor = cursor + 4
            end
            if (keyP["ptc_load"] ~= nil) then
                bodyBytes[cursor + 0] = 0xA0
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["ptc_load"]
                cursor = cursor + 4
            end
            if (keyP["left_down_real_wind_speed"] ~= nil) then
                bodyBytes[cursor + 0] = 0x07
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["left_down_real_wind_speed"]
                cursor = cursor + 4
            end
            if (keyP["right_up_real_wind_speed"] ~= nil) then
                bodyBytes[cursor + 0] = 0xA4
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["right_up_real_wind_speed"]
                cursor = cursor + 4
            end
            if (keyP["up_lr_wind_angle"] ~= nil) then
                bodyBytes[cursor + 0] = 0x0A
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["up_lr_wind_angle"]
                cursor = cursor + 4
            end
            if (keyP["swing_lr_under_angle"] ~= nil) then
                bodyBytes[cursor + 0] = 0x96
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["swing_lr_under_angle"]
                cursor = cursor + 4
            end
            if (keyP["right_ud_wind_angle"] ~= nil) then
                bodyBytes[cursor + 0] = 0xA1
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["right_ud_wind_angle"]
                cursor = cursor + 4
            end
            if (keyP["left_lr_wind_angle"] ~= nil) then
                bodyBytes[cursor + 0] = 0xA2
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["left_lr_wind_angle"]
                cursor = cursor + 4
            end
            if (keyP["right_lr_wind_angle"] ~= nil) then
                bodyBytes[cursor + 0] = 0xA3
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["right_lr_wind_angle"]
                cursor = cursor + 4
            end
            if (keyP["no_wind_sense_judge_param"] ~= nil) then
                bodyBytes[cursor + 0] = 0x9F
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["no_wind_sense_judge_param"]
                cursor = cursor + 4
            end
            if (keyP["jet_cool"] ~= nil) then
                bodyBytes[cursor + 0] = 0x67
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["jet_cool"]
                cursor = cursor + 4
            end
            if (keyP["wind_swing_ud_angle_switch"] ~= nil) then
                bodyBytes[cursor + 0] = 0x79
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x03
                bodyBytes[cursor + 3] = keyP["wind_swing_ud_angle_up"]
                bodyBytes[cursor + 4] = keyP["wind_swing_ud_angle_down"]
                bodyBytes[cursor + 5] = keyP["app_control_remember_ud"]
                cursor = cursor + 6
            end
            if (keyP["wind_swing_lr_angle_switch"] ~= nil) then
                bodyBytes[cursor + 0] = 0x7A
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x03
                bodyBytes[cursor + 3] = keyP["wind_swing_lr_angle_up"]
                bodyBytes[cursor + 4] = keyP["wind_swing_lr_angle_down"]
                bodyBytes[cursor + 5] = keyP["app_control_remember_lr"]
                cursor = cursor + 6
            end
            if (keyP["smart_dry_value"] ~= nil) then
                bodyBytes[cursor + 0] = 0x14
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["smart_dry_value"]
                cursor = cursor + 4
            end
            if (keyP["wind_swing_lr_under"] ~= nil) then
                bodyBytes[cursor + 0] = 0xAE
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["wind_swing_lr_under"]
                cursor = cursor + 4
            end
            if (keyP["screen_display_select"] ~= nil) then
                bodyBytes[cursor + 0] = 0x36
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["screen_display_select"]
                cursor = cursor + 4
            end
            if (keyP["no_wind_sense_updown_control"] ~= nil) then
                bodyBytes[cursor + 0] = 0xAF
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["no_wind_sense_up"]
                bodyBytes[cursor + 4] = keyP["no_wind_sense_down"]
                cursor = cursor + 5
            end
            if (keyP["auto_prevent_cold_wind"] ~= nil) then
                bodyBytes[cursor + 0] = 0x78
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["auto_prevent_cold_wind"]
                cursor = cursor + 4
            end
            if (keyP["linkage_2"] ~= nil) then
                bodyBytes[cursor + 0] = 0xB2
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["linkage_2"]
                cursor = cursor + 4
            end
            if (keyP["quick_cool_heat"] ~= nil) then
                bodyBytes[cursor + 0] = 0xB3
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["quick_cool_heat"]
                cursor = cursor + 4
            end
            if (keyP["cool_power_saving"] ~= nil) then
                bodyBytes[cursor + 0] = 0x89
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["cool_power_saving"]
                cursor = cursor + 4
            end
            if (keyP["prepare_food"] ~= nil) then
                bodyBytes[cursor + 0] = 0x54
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x03
                bodyBytes[cursor + 3] = keyP["prepare_food"]
                bodyBytes[cursor + 4] = 0xFF
                bodyBytes[cursor + 5] = 0xFF
                cursor = cursor + 6
            end
            if (keyP["quick_fry"] ~= nil) then
                bodyBytes[cursor + 0] = 0x55
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x03
                bodyBytes[cursor + 3] = keyP["quick_fry"]
                bodyBytes[cursor + 4] = 0xFF
                bodyBytes[cursor + 5] = 0xFF
                cursor = cursor + 6
            end
            if (keyP["quick_fry_control"] ~= nil) then
                bodyBytes[cursor + 0] = 0x8B
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["quick_fry_center_point"]
                bodyBytes[cursor + 4] = keyP["quick_fry_angle"]
                cursor = cursor + 5
            end
            if (keyP["dust_full_time_reset"] ~= nil) then
                bodyBytes[cursor + 0] = 0xB8
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["dust_full_time_reset"]
                cursor = cursor + 4
            end
            if (keyP["power_saving"] ~= nil) then
                bodyBytes[cursor + 0] = 0x62
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["power_saving"]
                cursor = cursor + 4
            end
            if (keyP["circle_fan"] ~= nil) then
                bodyBytes[cursor + 0] = 0xB9
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["circle_fan"]
                bodyBytes[cursor + 4] = keyP["circle_fan_mode"]
                cursor = cursor + 5
            end
            if (keyP["prevent_straight_wind_distance"] ~= nil) then
                bodyBytes[cursor + 0] = 0x38
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["prevent_straight_wind_distance"]
                cursor = cursor + 4
            end
            if (keyP["auto_prevent_cold_wind_memory"] ~= nil) then
                bodyBytes[cursor + 0] = 0xBC
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["auto_prevent_cold_wind_memory"]
                cursor = cursor + 4
            end
            if (keyP["linkage_2_temp_control_type"] ~= nil) then
                bodyBytes[cursor + 0] = 0xBB
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x05
                bodyBytes[cursor + 3] = keyP["linkage_2_temp_control_type"]
                bodyBytes[cursor + 4] = keyP["linkage_2_wind_control_type"]
                bodyBytes[cursor + 5] = keyP["linkage_2_fresh_air_control_type"]
                bodyBytes[cursor + 6] = keyP["linkage_2_purifier_control_type"]
                bodyBytes[cursor + 7] = keyP["linkage_2_humi_control_type"]
                cursor = cursor + 8
            end
            if (keyP["light_color_control"] ~= nil) then
                bodyBytes[cursor + 0] = 0xB7
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x13
                bodyBytes[cursor + 3] = 0
                bodyBytes[cursor + 3] = bit.bor(keyP["breath_cool"], bodyBytes[cursor + 3])
                bodyBytes[cursor + 3] = bit.bor(bit.lshift(keyP["breath_heat"], 1), bodyBytes[cursor + 3])
                bodyBytes[cursor + 3] = bit.bor(bit.lshift(keyP["breath_remove_odor"], 3), bodyBytes[cursor + 3])
                bodyBytes[cursor + 3] = bit.bor(bit.lshift(keyP["breath_fresh_air"], 4), bodyBytes[cursor + 3])
                bodyBytes[cursor + 3] = bit.bor(bit.lshift(keyP["breath_purifier"], 5), bodyBytes[cursor + 3])
                bodyBytes[cursor + 4] = keyP["cool_light_color_r"]
                bodyBytes[cursor + 5] = keyP["cool_light_color_g"]
                bodyBytes[cursor + 6] = keyP["cool_light_color_b"]
                bodyBytes[cursor + 7] = keyP["heat_light_color_r"]
                bodyBytes[cursor + 8] = keyP["heat_light_color_g"]
                bodyBytes[cursor + 9] = keyP["heat_light_color_b"]
                bodyBytes[cursor + 10] = keyP["dry_light_color_r"]
                bodyBytes[cursor + 11] = keyP["dry_light_color_g"]
                bodyBytes[cursor + 12] = keyP["dry_light_color_b"]
                bodyBytes[cursor + 13] = keyP["remove_odor_light_color_r"]
                bodyBytes[cursor + 14] = keyP["remove_odor_light_color_g"]
                bodyBytes[cursor + 15] = keyP["remove_odor_light_color_b"]
                bodyBytes[cursor + 16] = keyP["fresh_light_color_r"]
                bodyBytes[cursor + 17] = keyP["fresh_light_color_g"]
                bodyBytes[cursor + 18] = keyP["fresh_light_color_b"]
                bodyBytes[cursor + 19] = keyP["purifier_light_color_r"]
                bodyBytes[cursor + 20] = keyP["purifier_light_color_g"]
                bodyBytes[cursor + 21] = keyP["purifier_light_color_b"]
                cursor = cursor + 22
            end
            if (keyP["buzzer_off_status"] ~= nil) then
                bodyBytes[cursor + 0] = 0x2F
                bodyBytes[cursor + 1] = 0x02
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["buzzer_off_status"]
                cursor = cursor + 4
            end
            if (keyP["air_remove_odor"] ~= nil) then
                bodyBytes[cursor + 0] = 0xBF
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["air_remove_odor"]
                cursor = cursor + 4
            end
            if (keyP["clean_breath"] ~= nil) then
                bodyBytes[cursor + 0] = 0xC7
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x02
                bodyBytes[cursor + 3] = keyP["clean_breath"]
                bodyBytes[cursor + 4] = keyP["clean_breath_level"]
                cursor = cursor + 5
            end
            if (keyP["remove_arofene_clean"] ~= nil) then
                bodyBytes[cursor + 0] = 0xC8
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["remove_arofene_clean"]
                cursor = cursor + 4
            end
            if (keyP["health"] ~= nil) then
                bodyBytes[cursor + 0] = 0xC9
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["health"]
                cursor = cursor + 4
            end
            if (keyP["strong_cool"] ~= nil) then
                bodyBytes[cursor + 0] = 0xCA
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x01
                bodyBytes[cursor + 3] = keyP["strong_cool"]
                cursor = cursor + 4
            end
            if (keyP["humidification"] ~= nil) then
                bodyBytes[cursor + 0] = 0x75
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x03
                bodyBytes[cursor + 3] = keyP["humidification"]
                bodyBytes[cursor + 4] = keyP["humidification_fan_speed"]
                bodyBytes[cursor + 5] = keyP["humidification_mode"]
                cursor = cursor + 6
            end
            if (keyP["eco_time_status"] ~= nil) then
                bodyBytes[cursor + 0] = 0x1E
                bodyBytes[cursor + 1] = 0x00
                bodyBytes[cursor + 2] = 0x04
                bodyBytes[cursor + 3] = keyP["eco_time_switch"]
                bodyBytes[cursor + 4] = keyP["eco_time_sec"]
                bodyBytes[cursor + 5] = keyP["eco_time_min"]
                bodyBytes[cursor + 6] = keyP["eco_time_hour"]
                cursor = cursor + 7
            end
            math.randomseed(tostring(os.time() * #bodyBytes):reverse():sub(1, 7))
            math.random()
            bodyBytes[cursor] = math.random(1, 254)
            bodyBytes[cursor + 1] = crc8_854(bodyBytes, 0, cursor)
        end
        infoM = getTotalMsg(bodyBytes, keyB["BYTE_CONTROL_REQUEST"])
    end
    keyP["propertyNumber"] = 0
    keyP["prevent_super_cool"] = nil
    keyP["prevent_straight_wind"] = nil
    keyP["auto_prevent_straight_wind"] = nil
    keyP["wind_straight"] = nil
    keyP["wind_avoid"] = nil
    keyP["yb_wind_avoid"] = nil
    keyP["intelligent_wind"] = nil
    keyP["self_clean"] = nil
    keyP["no_wind_sense"] = nil
    keyP["no_wind_sense_level"] = nil
    keyP["fn_no_wind_sense"] = nil
    keyP["child_prevent_cold_wind"] = nil
    keyP["little_angel"] = nil
    keyP["cool_hot_sense"] = nil
    keyP["gentle_wind_sense"] = nil
    keyP["security"] = nil
    keyP["even_wind"] = nil
    keyP["single_tuyere"] = nil
    keyP["extreme_wind"] = nil
    keyP["extreme_wind_level"] = nil
    keyP["voice_control"] = nil
    keyP["pre_cool_hot"] = nil
    keyP["water_washing"] = nil
    keyP["fresh_air"] = nil
    keyP["fa_prevent_straight_wind"] = nil
    keyP["parent_control"] = nil
    keyP["parent_control_temp_up"] = nil
    keyP["parent_control_temp_down"] = nil
    keyP["nobody_energy_save"] = nil
    keyP["filter_value"] = nil
    keyP["filter_level"] = nil
    keyP["prevent_straight_wind_lr"] = nil
    keyP["pm25_value"] = nil
    keyP["water_pump"] = nil
    keyP["intelligent_control"] = nil
    keyP["wind_swing_ud_angle"] = nil
    keyP["wind_swing_lr_angle"] = nil
    keyP["volume_control"] = nil
    keyP["voice_control_new"] = nil
    keyP["face_register"] = nil
    keyP["cool_temp_up"] = nil
    keyP["cool_temp_down"] = nil
    keyP["auto_temp_up"] = nil
    keyP["auto_temp_down"] = nil
    keyP["heat_temp_up"] = nil
    keyP["heat_temp_down"] = nil
    keyP["remote_control_lock"] = nil
    keyP["remote_control_lock_control"] = nil
    keyP["operating_time"] = nil
    -- keyP["indoor_humidity"] = nil  -- preserve C1/0x45 value across messages
    keyP["degerming"] = nil
    keyP["wind_top"] = nil
    keyP["wind_around"] = nil
    keyP["wind_around_ud"] = nil
    keyP["child_lock"] = nil
    keyP["buzzer_all"] = nil
    keyP["self_remove_odor_phase"] = nil
    keyP["high_temp_remove_odor_alone"] = nil
    keyP["power_lock"] = nil
    keyP["ptc_lock"] = nil
    keyP["offline_operating_time"] = nil
    keyP["ozone"] = nil
    keyP["soft_warm"] = nil
    keyP["fresh_air_parm"] = nil
    keyP["rewarming_dry"] = nil
    keyP["new_mode_power"] = nil
    keyP["new_mode"] = nil
    keyP["new_temperature"] = nil
    keyP["new_wind_speed"] = nil
    keyP["uvc_remove_odor"] = nil
    keyP["uvc_power_off"] = nil
    keyP["humidification"] = nil
    keyP["humidification_fan_speed"] = nil
    keyP["humidification_mode"] = nil
    keyP["remove_odor"] = nil
    keyP["remove_odor_fan_speed"] = nil
    keyP["whirl_wind_left"] = nil
    keyP["whirl_wind_right"] = nil
    keyP["inner_purifier"] = nil
    keyP["inner_purifier_fan_speed"] = nil
    keyP["inner_purifier_mode"] = nil
    keyP["fresh_air_mode_two"] = nil
    keyP["wind_speed_right"] = nil
    keyP["fresh_air_on_co2"] = nil
    keyP["fresh_air_off_co2"] = nil
    keyP["gentle_wind_enable"] = nil
    keyP["linkage"] = nil
    keyP["moisturizing"] = nil
    keyP["moisturizing_fan_speed"] = nil
    keyP["no_wind_sense_left"] = nil
    keyP["no_wind_sense_right"] = nil
    keyP["no_wind_sense_control"] = nil
    keyP["is_query"] = nil
    keyP["timerSignal"] = 0
    keyP["powerValue"] = nil
    keyP["modeValue"] = nil
    keyP["smartDryValue"] = nil
    keyP["temperature"] = nil
    keyP["smallTemperature"] = nil
    keyP["indoorTemperatureValue"] = nil
    keyP["smallIndoorTemperatureValue"] = nil
    keyP["outdoorTemperatureValue"] = nil
    keyP["smallOutdoorTemperatureValue"] = nil
    keyP["fanspeedValue"] = nil
    keyP["closeTimerSwitch"] = nil
    keyP["openTimerSwitch"] = nil
    keyP["closeHour"] = nil
    keyP["closeStepMintues"] = nil
    keyP["closeMin"] = nil
    keyP["closeTime"] = nil
    keyP["openHour"] = nil
    keyP["openStepMintues"] = nil
    keyP["openMin"] = nil
    keyP["openTime"] = nil
    keyP["strongWindValue"] = nil
    keyP["comfortableSleepValue"] = nil
    keyP["comfortableSleepSwitch"] = nil
    keyP["comfortableSleepTime"] = nil
    keyP["comfort_sleep_curve"] = nil
    keyP["PTCValue"] = nil
    keyP["purifierValue"] = nil
    keyP["ecoValue"] = nil
    keyP["dryValue"] = nil
    keyP["swingLRValue"] = nil
    keyP["swingUDValue"] = nil
    keyP["swingLRValueUnder"] = nil
    keyP["swingLRUnderSwitch"] = 0
    keyP["currentWorkTime"] = nil
    keyP["PTCForceValue"] = 0
    keyP["screenDisplayNowValue"] = nil
    keyP["wind_swing_ud_right"] = nil
    keyP["wind_swing_lr_right"] = nil
    keyP["wind_swing_lr_left"] = nil
    keyP["wind_swing_ud_left"] = nil
    keyP["screen_display"] = nil
    keyP["ptc_default_rule"] = nil
    keyP["five_dimension_mode"] = nil
    keyP["total_status_switch"] = nil
    keyP["screen_display_time"] = nil
    keyP["wait_clean"] = nil
    keyP["self_clean_time"] = nil
    keyP["dry_clean_time"] = nil
    keyP["ptc_load"] = nil
    keyP["defrosting_load"] = nil
    keyP["no_wind_sense_judge_param"] = nil
    keyP["left_down_real_wind_speed"] = nil
    keyP["real_mode"] = nil
    keyP["right_up_real_wind_speed"] = nil
    keyP["left_ud_wind_angle"] = nil
    keyP["up_lr_wind_angle"] = nil
    keyP["swing_lr_under_angle"] = nil
    keyP["right_ud_wind_angle"] = nil
    keyP["left_lr_wind_angle"] = nil
    keyP["right_lr_wind_angle"] = nil
    keyP["jet_cool"] = nil
    keyP["wind_swing_ud_angle_up"] = nil
    keyP["wind_swing_ud_angle_down"] = nil
    keyP["app_control_remember_ud"] = nil
    keyP["wind_swing_lr_angle_up"] = nil
    keyP["wind_swing_lr_angle_down"] = nil
    keyP["app_control_remember_lr"] = nil
    keyP["smart_dry_value"] = nil
    keyP["no_wind_sense_down"] = nil
    keyP["no_wind_sense_up"] = nil
    keyP["no_wind_sense_updown_control"] = nil
    keyP["auto_prevent_cold_wind"] = nil
    keyP["cool_power_saving"] = nil
    keyP["prepare_food"] = nil
    keyP["quick_fry"] = nil
    keyP["quick_fry_temp"] = nil
    keyP["quick_fry_fan_speed"] = nil
    keyP["quick_fry_center_point"] = nil
    keyP["quick_fry_angle"] = nil
    keyP["quick_fry_control"] = nil
    keyP["light_color_control"] = nil
    keyP["dust_full_time_reset"] = nil
    keyP["circle_fan"] = nil
    keyP["circle_fan_mode"] = nil
    keyP["power_saving"] = nil
    keyP["linkage_2_temp_auto"] = nil
    keyP["linkage_2_wind_auto"] = nil
    keyP["linkage_2_fresh_air_auto"] = nil
    keyP["linkage_2_purifier_auto"] = nil
    keyP["linkage_2_humi_auto"] = nil
    keyP["linkage_2_temp_control_type"] = nil
    keyP["linkage_2_wind_control_type"] = nil
    keyP["linkage_2_fresh_air_control_type"] = nil
    keyP["linkage_2_purifier_control_type"] = nil
    keyP["linkage_2_humi_control_type"] = nil
    keyP["light"] = nil
    keyP["eco_time_status"] = nil
    propertyPre = nil
    local ret = table2string(infoM)
    ret = string2hexstring(ret)
    return ret
end

function dataToJson(jsonCmd)
    init_keyP()
    if (not jsonCmd) then return nil end
    local json = decode(jsonCmd)
    local deviceinfo = json["deviceinfo"]
    deviceSubType = deviceinfo["deviceSubType"]
    local deviceSN = json["deviceinfo"]["deviceSN"]
    if deviceSN ~= nil then deviceSN8 = string.sub(deviceSN, 13, 17) end
    local status = json["status"]
    if (status) then jsonToModel(status, "status") end
    local binData = json["msg"]["data"]
    local info = {}
    local msgBytes = {}
    local bodyBytes = {}
    local msgLength = 0
    local bodyLength = 0
    info = string2table(binData)
    dataType = info[10]; for i = 1, #info do msgBytes[i - 1] = info[i] end
    msgLength = msgBytes[1]
    bodyLength = msgLength - keyB["BYTE_PROTOCOL_LENGTH"] - 1
    for i = 0, bodyLength do bodyBytes[i] = msgBytes[i + keyB["BYTE_PROTOCOL_LENGTH"]] end
    binToModel(bodyBytes, deviceSN8)
    local streams = {}
    streams[keyT["KEY_VERSION"]] = keyV["VALUE_VERSION"]
    if (keyP["powerValue"] ~= nil) then
        print(keyP["powerValue"])
        if (keyP["powerValue"] == keyB["BYTE_POWER_ON"]) then
            print(keyP["powerValue"])
            streams[keyT["KEY_POWER"]] = keyV["VALUE_FUNCTION_ON"]
        elseif (keyP["powerValue"] == keyB["BYTE_POWER_OFF"]) then streams[keyT["KEY_POWER"]] = keyV
            ["VALUE_FUNCTION_OFF"] else streams[keyT["KEY_POWER"]] = keyV["VALUE_FUNCTION_OFF"] end
    end
    if (keyP["modeValue"] ~= nil) then if (keyP["modeValue"] == keyB["BYTE_MODE_HEAT"]) then streams[keyT["KEY_MODE"]] =
            keyV["VALUE_MODE_HEAT"] elseif (keyP["modeValue"] == keyB["BYTE_MODE_COOL"]) then streams[keyT["KEY_MODE"]] =
            keyV["VALUE_MODE_COOL"] elseif (keyP["modeValue"] == keyB["BYTE_MODE_AUTO"]) then streams[keyT["KEY_MODE"]] =
            keyV["VALUE_MODE_AUTO"] elseif (keyP["modeValue"] == keyB["BYTE_MODE_DRY"]) then streams[keyT["KEY_MODE"]] =
            keyV["VALUE_MODE_DRY"] elseif (keyP["modeValue"] == keyB["BYTE_MODE_FAN"]) then streams[keyT["KEY_MODE"]] =
            keyV["VALUE_MODE_FAN"] elseif (keyP["modeValue"] == keyB["BYTE_MODE_SMART_DRY"]) then
            streams[keyT["KEY_MODE"]] = keyV["VALUE_MODE_SMART_DRY"]
            if (keyP["smartDryValue"] ~= nil and keyP["smartDryValue"] >= 30 and keyP["smartDryValue"] <= 101) then streams[keyT["KEY_SMART_DRY"]] =
                keyP["smartDryValue"] end
        end end
    if (keyP["purifierValue"] ~= nil) then if (keyP["purifierValue"] == keyB["BYTE_PURIFIER_ON"]) then streams[keyT["KEY_PURIFIER"]] =
            keyV["VALUE_FUNCTION_ON"] elseif (keyP["purifierValue"] == keyB["BYTE_PURIFIER_OFF"]) then streams[keyT["KEY_PURIFIER"]] =
            keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["ecoValue"] ~= nil) then if (keyP["ecoValue"] == keyB["BYTE_ECO_ON"] or keyP["ecoValue"] == 0x01) then streams[keyT["KEY_ECO"]] =
            keyV["VALUE_FUNCTION_ON"] elseif (keyP["ecoValue"] == keyB["BYTE_ECO_OFF"]) then streams[keyT["KEY_ECO"]] =
            keyV["VALUE_FUNCTION_OFF"] end end
    if ((keyP["dryValue"] ~= nil) and (keyP["modeValue"] ~= nil)) then if (keyP["dryValue"] == keyB["BYTE_DRY_ON"]) then streams[keyT["KEY_DRY"]] =
            keyV["VALUE_FUNCTION_ON"] else streams[keyT["KEY_DRY"]] = keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["fanspeedValue"] ~= nil) then streams[keyT["KEY_FANSPEED"]] = keyP["fanspeedValue"] end
    if (keyP["wind_speed_right"] ~= nil) then streams["wind_speed_right"] = keyP["wind_speed_right"] end
    if ((keyP["outdoorTemperatureValue"] ~= nil) and (keyP["smallOutdoorTemperatureValue"] ~= nil)) then
        local t1, t2 = math.modf(keyP["outdoorTemperatureValue"])
        if (keyP["outdoorTemperatureValue"] < 0) then streams[keyV["VALUE_OUTDOOR_TEMPERATURE"]] = t1 -
            keyP["smallOutdoorTemperatureValue"] / 10 else streams[keyV["VALUE_OUTDOOR_TEMPERATURE"]] = t1 +
            keyP["smallOutdoorTemperatureValue"] / 10 end
    end
    if (keyP["outdoor_temperature"] ~= nil) then streams["outdoor_temperature"] = keyP["outdoor_temperature"] / 100 end
    if ((keyP["indoorTemperatureValue"] ~= nil) and (keyP["smallIndoorTemperatureValue"] ~= nil)) then
        local t1, t2 = math.modf(keyP["indoorTemperatureValue"])
        if (keyP["indoorTemperatureValue"] < 0) then streams[keyV["VALUE_INDOOR_TEMPERATURE"]] = t1 -
            keyP["smallIndoorTemperatureValue"] / 10 else streams[keyV["VALUE_INDOOR_TEMPERATURE"]] = t1 +
            keyP["smallIndoorTemperatureValue"] / 10 end
    end
    if (keyP["swingUDValue"] ~= nil) then if (keyP["swingUDValue"] == keyB["BYTE_SWING_UD_ON"]) then streams[keyT["KEY_SWING_UD"]] =
            keyV["VALUE_FUNCTION_ON"] elseif (keyP["swingUDValue"] == keyB["BYTE_SWING_UD_OFF"]) then streams[keyT["KEY_SWING_UD"]] =
            keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["swingLRValue"] ~= nil) then if (keyP["swingLRValue"] == keyB["BYTE_SWING_LR_ON"]) then streams[keyT["KEY_SWING_LR"]] =
            keyV["VALUE_FUNCTION_ON"] elseif (keyP["swingLRValue"] == keyB["BYTE_SWING_LR_OFF"]) then streams[keyT["KEY_SWING_LR"]] =
            keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["swingLRValueUnder"] == keyB["BYTE_SWING_LR_UNDER_ON"] or keyP["swingLRValueUnder"] == 0x40) then streams[keyT["KEY_SWING_LR_UNDER"]] =
        keyV["VALUE_FUNCTION_ON"] elseif (keyP["swingLRValueUnder"] == keyB["BYTE_SWING_LR_UNDER_OFF"]) then streams[keyT["KEY_SWING_LR_UNDER"]] =
        keyV["VALUE_FUNCTION_OFF"] end
    if (keyP["wind_swing_lr_under"] ~= nil) then if (keyP["wind_swing_lr_under"] == 1) then streams["wind_swing_lr_under"] =
            "on" else streams["wind_swing_lr_under"] = "off" end end
    if ((keyP["PTCValue"] ~= nil)) then if (keyP["PTCValue"] == keyB["BYTE_PTC_ON"]) then streams[keyT["KEY_PTC"]] = keyV
            ["VALUE_FUNCTION_ON"] else streams[keyT["KEY_PTC"]] = keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["ptc_default_rule"] ~= nil) then streams["ptc_default_rule"] = keyP["ptc_default_rule"] end
    if (keyP["openTimerSwitch"] ~= nil) then if (keyP["openTimerSwitch"] == keyB["BYTE_START_TIMER_SWITCH_ON"]) then streams[keyT["KEY_TIME_ON"]] =
            keyV["VALUE_FUNCTION_ON"] elseif (keyP["openTimerSwitch"] == keyB["BYTE_START_TIMER_SWITCH_OFF"]) then streams[keyT["KEY_TIME_ON"]] =
            keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["closeTimerSwitch"] ~= nil) then if (keyP["closeTimerSwitch"] == keyB["BYTE_CLOSE_TIMER_SWITCH_ON"]) then streams[keyT["KEY_TIME_OFF"]] =
            keyV["VALUE_FUNCTION_ON"] elseif (keyP["closeTimerSwitch"] == keyB["BYTE_CLOSE_TIMER_SWITCH_OFF"]) then streams[keyT["KEY_TIME_OFF"]] =
            keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["closeTimerSwitch"] ~= nil) then if (keyP["closeTimerSwitch"] == keyB["BYTE_CLOSE_TIMER_SWITCH_OFF"]) then streams[keyT["KEY_CLOSE_TIME"]] = 0 else streams[keyT["KEY_CLOSE_TIME"]] =
            keyP["closeTime"] end end
    if (keyP["openTimerSwitch"] ~= nil) then if (keyP["openTimerSwitch"] == keyB["BYTE_START_TIMER_SWITCH_OFF"]) then streams[keyT["KEY_OPEN_TIME"]] = 0 else streams[keyT["KEY_OPEN_TIME"]] =
            keyP["openTime"] end end
    if (keyP["currentWorkTime"] ~= nil) then streams[keyT["KEY_CURRENT_WORK_TIME"]] = keyP["currentWorkTime"] end
    if (keyP["strongWindValue"] ~= nil) then if (keyP["strongWindValue"] == keyB["BYTE_STRONG_WIND_ON"]) then streams[keyT["KEY_STRONG_WIND"]] =
            keyV["VALUE_FUNCTION_ON"] elseif (keyP["strongWindValue"] == keyB["BYTE_STRONG_WIND_OFF"]) then streams[keyT["KEY_STRONG_WIND"]] =
            keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["power_saving"] ~= nil) then if (keyP["power_saving"] == 0x08 or keyP["power_saving"] == 0x01) then streams["power_saving"] =
            keyV["VALUE_FUNCTION_ON"] elseif (keyP["power_saving"] == 0x00) then streams["power_saving"] = keyV
            ["VALUE_FUNCTION_OFF"] end end
    if (keyP["temperature"] ~= nil) then streams[keyT["KEY_TEMPERATURE"]] = keyP["temperature"] end
    if (keyP["smallTemperature"] ~= nil) then if (keyP["smallTemperature"] == 0x01) then streams["small_temperature"] = 0.5 else streams["small_temperature"] = 0 end end
    streams[keyT["KEY_ERROR_CODE"]] = keyP["errorCode"]
    if (keyP["kickQuilt"] ~= nil) then if (keyP["kickQuilt"] == 0x00) then streams["kick_quilt"] = "off" elseif (keyP["kickQuilt"] == 0x01) then streams["kick_quilt"] =
            "on" end end
    if (keyP["comfortPowerSave"] ~= nil) then if (keyP["comfortPowerSave"] == 0x00) then streams["comfort_power_save"] =
            "off" elseif (keyP["comfortPowerSave"] == 0x01) then streams["comfort_power_save"] = "on" end end
    if (keyP["no_wind_sense"] ~= nil) then streams["no_wind_sense"] = keyP["no_wind_sense"] end
    if (keyP["fn_no_wind_sense"] ~= nil) then if (keyP["fn_no_wind_sense"] == 0x00) then streams["fn_no_wind_sense"] =
            "off" elseif (keyP["fn_no_wind_sense"] == 0x01) then streams["fn_no_wind_sense"] = "on" end end
    if (keyP["no_wind_sense_level"] ~= nil) then streams["no_wind_sense_level"] = keyP["no_wind_sense_level"] end
    if (keyP["preventCold"] ~= nil) then if (keyP["preventCold"] == 0x00) then streams["prevent_cold"] = "off" elseif (keyP["preventCold"] == 0x01) then streams["prevent_cold"] =
            "on" end end
    if (keyP["comfortableSleepValue"] ~= nil) then if (keyP["comfortableSleepValue"] == 0x00) then streams["comfort_sleep"] =
            "off" elseif (keyP["comfortableSleepValue"] == 0x03) then streams["comfort_sleep"] = "on" end end
    if (keyP["screen_display"] ~= nil) then streams["screen_display"] = keyP["screen_display"] end
    if (keyP["screenDisplayNowValue"] ~= nil) then if (keyP["screenDisplayNowValue"] == 0x07) then
            streams["screen_display_now"] = "off"
            streams["screen_display"] = 0
        else
            streams["screen_display_now"] = "on"
            streams["screen_display"] = 100
        end end
    if (keyP["naturalWind"] ~= nil) then if (keyP["naturalWind"] == 0x02 or keyP["naturalWind"] == 0x40) then streams["natural_wind"] =
            "on" elseif (keyP["naturalWind"] == 0x00) then streams["natural_wind"] = "off" end end
    if (keyP["pmv"] ~= nil) then streams["pmv"] = keyP["pmv"] end
    if (keyP["fresh_filter_time_total"] ~= nil) then streams["fresh_filter_time_total"] = keyP
        ["fresh_filter_time_total"] end
    if (keyP["fresh_filter_time_use"] ~= nil) then streams["fresh_filter_time_use"] = keyP["fresh_filter_time_use"] end
    if (keyP["fresh_filter_timeout"] ~= nil) then streams["fresh_filter_timeout"] = keyP["fresh_filter_timeout"] end
    if (keyP["electrify_time_day"] ~= nil) then streams["electrify_time_day"] = keyP["electrify_time_day"] end
    if (keyP["electrify_time_hour"] ~= nil) then streams["electrify_time_hour"] = keyP["electrify_time_hour"] end
    if (keyP["electrify_time_min"] ~= nil) then streams["electrify_time_min"] = keyP["electrify_time_min"] end
    if (keyP["electrify_time_second"] ~= nil) then streams["electrify_time_second"] = keyP["electrify_time_second"] end
    if (keyP["total_operating_time_day"] ~= nil) then streams["total_operating_time_day"] = keyP
        ["total_operating_time_day"] end
    if (keyP["total_operating_time_hour"] ~= nil) then streams["total_operating_time_hour"] = keyP
        ["total_operating_time_hour"] end
    if (keyP["total_operating_time_min"] ~= nil) then streams["total_operating_time_min"] = keyP
        ["total_operating_time_min"] end
    if (keyP["total_operating_time_second"] ~= nil) then streams["total_operating_time_second"] = keyP
        ["total_operating_time_second"] end
    if (keyP["current_operating_time_day"] ~= nil) then streams["current_operating_time_day"] = keyP
        ["current_operating_time_day"] end
    if (keyP["current_operating_time_hour"] ~= nil) then streams["current_operating_time_hour"] = keyP
        ["current_operating_time_hour"] end
    if (keyP["current_operating_time_min"] ~= nil) then streams["current_operating_time_min"] = keyP
        ["current_operating_time_min"] end
    if (keyP["current_operating_time_second"] ~= nil) then streams["current_operating_time_second"] = keyP
        ["current_operating_time_second"] end
    if (keyP["total_power_consumption"] ~= nil) then streams["total_power_consumption"] = keyP
        ["total_power_consumption"] end
    if (keyP["total_operating_consumption"] ~= nil) then streams["total_operating_consumption"] = keyP
        ["total_operating_consumption"] end
    if (keyP["current_operating_consumption"] ~= nil) then streams["current_operating_consumption"] = keyP
        ["current_operating_consumption"] end
    if (keyP["current_time_power"] ~= nil) then streams["current_time_power"] = keyP["current_time_power"] end
    if (keyP["analysis_value"] ~= nil) then streams["analysis_value"] = keyP["analysis_value"] end
    if (keyP["t2_temp"] ~= nil) then streams["t2_temp"] = keyP["t2_temp"] end
    if (keyP["dust_full_time"] ~= nil) then streams["dust_full_time"] = keyP["dust_full_time"] end
    if (keyP["fault_tag"] ~= nil) then streams["fault_tag"] = keyP["fault_tag"] end
    if (keyP["arom_old"] ~= nil) then streams["arom_old"] = keyP["arom_old"] end
    if (keyP["wind_swing_lr_left"] ~= nil) then if (keyP["wind_swing_lr_left"] == 0x01) then streams["wind_swing_lr_left"] =
            keyV["VALUE_FUNCTION_ON"] else streams["wind_swing_lr_left"] = keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["wind_swing_lr_right"] ~= nil) then if (keyP["wind_swing_lr_right"] == 0x01) then streams["wind_swing_lr_right"] =
            keyV["VALUE_FUNCTION_ON"] else streams["wind_swing_lr_right"] = keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["wind_swing_ud_left"] ~= nil) then if (keyP["wind_swing_ud_left"] == 0x01) then streams["wind_swing_ud_left"] =
            keyV["VALUE_FUNCTION_ON"] else streams["wind_swing_ud_left"] = keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["wind_swing_ud_right"] ~= nil) then if (keyP["wind_swing_ud_right"] == 0x01) then streams["wind_swing_ud_right"] =
            keyV["VALUE_FUNCTION_ON"] else streams["wind_swing_ud_right"] = keyV["VALUE_FUNCTION_OFF"] end end
    if (keyP["rewarming_dry"] ~= nil) then streams["rewarming_dry"] = keyP["rewarming_dry"] end
    if (keyP["whirl_wind_left"] ~= nil) then streams["whirl_wind_left"] = keyP["whirl_wind_left"] end
    if (keyP["whirl_wind_right"] ~= nil) then streams["whirl_wind_right"] = keyP["whirl_wind_right"] end
    if (keyP["indoor_co2"] ~= nil) then streams["indoor_co2"] = keyP["indoor_co2"] end
    if (keyP["linkage_fan_speed"] ~= nil) then streams["linkage_fan_speed"] = keyP["linkage_fan_speed"] end
    if (keyP["prevent_super_cool"] ~= nil) then if (keyP["prevent_super_cool"] == 0x00) then streams["prevent_super_cool"] =
            "off" elseif (keyP["prevent_super_cool"] == 0x01) then streams["prevent_super_cool"] = "on" end end
    if (keyP["prevent_straight_wind"] ~= nil) then streams["prevent_straight_wind"] = keyP["prevent_straight_wind"] end
    if (keyP["fa_prevent_straight_wind"] ~= nil) then streams["fa_prevent_straight_wind"] = keyP
        ["fa_prevent_straight_wind"] end
    if (keyP["auto_prevent_straight_wind"] ~= nil) then if (keyP["auto_prevent_straight_wind"] == 0x00) then streams["auto_prevent_straight_wind"] =
            "off" elseif (keyP["auto_prevent_straight_wind"] == 0x01) then streams["auto_prevent_straight_wind"] = "on" end end
    if (keyP["self_clean"] ~= nil) then if (keyP["self_clean"] == 0x00) then streams["self_clean"] = "off" elseif (keyP["self_clean"] == 0x01) then streams["self_clean"] =
            "on" end end
    if (keyP["wind_straight"] ~= nil) then if (keyP["wind_straight"] == 0x00) then streams["wind_straight"] = "off" elseif (keyP["wind_straight"] == 0x01) then streams["wind_straight"] =
            "on" end end
    if (keyP["yb_wind_avoid"] ~= nil) then if (keyP["yb_wind_avoid"] == 0x00) then streams["yb_wind_avoid"] = "off" elseif (keyP["yb_wind_avoid"] == 0x02) then streams["yb_wind_avoid"] =
            "on" end end
    if (keyP["wind_avoid"] ~= nil) then if (keyP["wind_avoid"] == 0x00) then streams["wind_avoid"] = "off" elseif (keyP["wind_avoid"] == 0x01 or keyP["wind_avoid"] == 0x02) then streams["wind_avoid"] =
            "on" end end
    if (keyP["intelligent_wind"] ~= nil) then if (keyP["intelligent_wind"] == 0x00) then streams["intelligent_wind"] =
            "off" elseif (keyP["intelligent_wind"] == 0x01) then streams["intelligent_wind"] = "on" end end
    if (keyP["child_prevent_cold_wind"] ~= nil) then if (keyP["child_prevent_cold_wind"] == 0x00) then streams["child_prevent_cold_wind"] =
            "off" elseif (keyP["child_prevent_cold_wind"] == 0x01) then streams["child_prevent_cold_wind"] = "on" end end
    if (keyP["no_wind_sense"] ~= nil) then streams["no_wind_sense"] = keyP["no_wind_sense"] end
    if (keyP["fn_no_wind_sense"] ~= nil) then if (keyP["fn_no_wind_sense"] == 0x00) then streams["fn_no_wind_sense"] =
            "off" elseif (keyP["fn_no_wind_sense"] == 0x01) then streams["fn_no_wind_sense"] = "on" end end
    if (keyP["no_wind_sense_level"] ~= nil) then streams["no_wind_sense_level"] = keyP["no_wind_sense_level"] end
    if (keyP["little_angel"] ~= nil) then if (keyP["little_angel"] == 0x00) then streams["little_angel"] = "off" elseif (keyP["little_angel"] == 0x01) then streams["little_angel"] =
            "on" end end
    if (keyP["cool_hot_sense"] ~= nil) then if (keyP["cool_hot_sense"] == 0x00) then streams["cool_hot_sense"] = "off" elseif (keyP["cool_hot_sense"] == 0x01) then streams["cool_hot_sense"] =
            "on" end end
    if (keyP["gentle_wind_sense"] ~= nil) then if (keyP["gentle_wind_sense"] == 0x00) then streams["gentle_wind_sense"] =
            "off" elseif (keyP["gentle_wind_sense"] == 0x01) then streams["gentle_wind_sense"] = "on" end end
    if (keyP["security"] ~= nil) then if (keyP["security"] == 0x00) then streams["security"] = "off" elseif (keyP["security"] == 0x01) then streams["security"] =
            "on" end end
    if (keyP["even_wind"] ~= nil) then if (keyP["even_wind"] == 0x00) then streams["even_wind"] = "off" elseif (keyP["even_wind"] == 0x01) then streams["even_wind"] =
            "on" end end
    if (keyP["single_tuyere"] ~= nil) then if (keyP["single_tuyere"] == 0x00) then streams["single_tuyere"] = "off" elseif (keyP["single_tuyere"] == 0x01) then streams["single_tuyere"] =
            "on" end end
    if (keyP["extreme_wind"] ~= nil) then
        if (keyP["extreme_wind"] == 0x00) then streams["extreme_wind"] = "off" elseif (keyP["extreme_wind"] == 0x01) then streams["extreme_wind"] =
            "on" end
        streams["extreme_wind_level"] = keyP["extreme_wind_level"]
    end
    if (keyP["degerming"] ~= nil) then if (keyP["degerming"] == 0x00) then streams["degerming"] = "off" elseif (keyP["degerming"] == 0x01) then streams["degerming"] =
            "on" end end
    if (keyP["light"] ~= nil) then
        streams["light"] = keyP["light"]
        if (keyP["light"] == 1) then streams["light"] = 100 end
    end
    if (keyP["wind_top"] ~= nil) then if (keyP["wind_top"] == 0x00) then streams["wind_top"] = "off" elseif (keyP["wind_top"] == 0x01) then streams["wind_top"] =
            "on" end end
    if (keyP["wind_around"] ~= nil) then if (keyP["wind_around"] == 0x00) then streams["wind_around"] = "off" elseif (keyP["wind_around"] == 0x01) then streams["wind_around"] =
            "on" elseif (keyP["wind_around"] == 0x02) then streams["wind_around"] = "on" end end
    if (keyP["wind_around_ud"] ~= nil) then streams["wind_around_ud"] = keyP["wind_around_ud"] end
    if (keyP["wind_swing_lr_angle"] ~= nil) then streams["wind_swing_lr_angle"] = keyP["wind_swing_lr_angle"] end
    if (keyP["wind_swing_ud_angle"] ~= nil) then streams["wind_swing_ud_angle"] = keyP["wind_swing_ud_angle"] end
    if (keyP["voice_control"] ~= nil) then if (keyP["voice_control"] == 0x00) then streams["voice_control"] = "off" elseif (keyP["voice_control"] == 0x03) then streams["voice_control"] =
            "on" end end
    if (keyP["pre_cool_hot"] ~= nil) then if (keyP["pre_cool_hot"] == 0x00) then streams["pre_cool_hot"] = "off" elseif (keyP["pre_cool_hot"] == 0x01) then streams["pre_cool_hot"] =
            "on" end end
    if (keyP["water_washing"] ~= nil) then
        if (keyP["water_washing"] == 0x01) then streams["water_washing"] = "on" elseif (keyP["water_washing"] == 0x00) then streams["water_washing"] =
            "off" end
        streams["water_washing_manual"] = keyP["water_washing_manual"]
        streams["water_washing_time"] = keyP["water_washing_time"]
        streams["water_washing_stage"] = keyP["water_washing_stage"]
    end
    if (keyP["fresh_air"] ~= nil) then
        if (keyP["fresh_air"] == 0x00) then streams["fresh_air"] = "off" elseif (keyP["fresh_air"] == 0x01) then streams["fresh_air"] =
            "on" elseif (keyP["fresh_air"] == 0x03) then streams["fresh_air"] = "on" end
        streams["fresh_air_fan_speed"] = keyP["fresh_air_fan_speed"]
        streams["fresh_air_temp"] = keyP["fresh_air_temp"]
    end
    if (keyP["fresh_air_mode_two"] ~= nil) then streams["fresh_air_mode_two"] = keyP["fresh_air_mode_two"] end
    if (keyP["fresh_air_mode"] ~= nil) then streams["fresh_air_mode"] = keyP["fresh_air_mode"] end
    if (keyP["parent_control"] ~= nil) then
        if (keyP["parent_control"] == 0x00) then streams["parent_control"] = "off" elseif (keyP["parent_control"] == 0x01) then streams["parent_control"] =
            "on" end
        streams["parent_control_temp_up"] = keyP["parent_control_temp_up"]
        streams["parent_control_temp_down"] = keyP["parent_control_temp_down"]
    end
    if (keyP["nobody_energy_save"] ~= nil) then if (keyP["nobody_energy_save"] == 0x00) then streams["nobody_energy_save"] =
            "off" elseif (keyP["nobody_energy_save"] == 0x01) then streams["nobody_energy_save"] = "on" end end
    if (keyP["filter_value"] ~= nil) then
        streams["filter_value"] = keyP["filter_value"]
        streams["filter_level"] = keyP["filter_level"]
    end
    if (keyP["prevent_straight_wind_lr"] ~= nil) then streams["prevent_straight_wind_lr"] = keyP
        ["prevent_straight_wind_lr"] end
    if (keyP["pm25_value"] ~= nil) then streams["pm25_value"] = keyP["pm25_value"] end
    if (keyP["water_pump"] ~= nil) then if (keyP["water_pump"] == 0x00) then streams["water_pump"] = "off" elseif (keyP["water_pump"] == 0x01) then streams["water_pump"] =
            "on" end end
    if (keyP["intelligent_control"] ~= nil) then if (keyP["intelligent_control"] == 0x00) then streams["intelligent_control"] =
            "off" elseif (keyP["intelligent_control"] == 0x01) then streams["intelligent_control"] = "on" end end
    if (keyP["volume_control"] ~= nil) then streams["volume_control"] = keyP["volume_control"] end
    if (keyP["voice_control_new"] ~= nil) then streams["voice_control_new"] = keyP["voice_control_new"] end
    if (keyP["face_register"] ~= nil) then streams["face_register"] = keyP["face_register"] end
    if (keyP["cool_temp_up"] ~= nil) then streams["cool_temp_up"] = keyP["cool_temp_up"] end
    if (keyP["cool_temp_down"] ~= nil) then streams["cool_temp_down"] = keyP["cool_temp_down"] end
    if (keyP["auto_temp_up"] ~= nil) then streams["auto_temp_up"] = keyP["auto_temp_up"] end
    if (keyP["auto_temp_down"] ~= nil) then streams["auto_temp_down"] = keyP["auto_temp_down"] end
    if (keyP["heat_temp_up"] ~= nil) then streams["heat_temp_up"] = keyP["heat_temp_up"] end
    if (keyP["heat_temp_down"] ~= nil) then streams["heat_temp_down"] = keyP["heat_temp_down"] end
    if (keyP["remote_control_lock"] ~= nil) then streams["remote_control_lock"] = keyP["remote_control_lock"] end
    if (keyP["remote_control_lock_control"] ~= nil) then streams["remote_control_lock_control"] = keyP
        ["remote_control_lock_control"] end
    if (keyP["operating_time"] ~= nil) then streams["operating_time"] = keyP["operating_time"] end
    if (keyP["indoor_humidity"] ~= nil) then streams["indoor_humidity"] = keyP["indoor_humidity"] end
    if (keyP["child_lock"] ~= nil) then streams["child_lock"] = keyP["child_lock"] end
    if (keyP["is_query"] ~= nil) then streams["is_query"] = keyP["is_query"] end
    if (keyP["analysis_value"] ~= nil) then streams["analysis_value"] = keyP["analysis_value"] end
    if (keyP["buzzer_all"] ~= nil) then streams["buzzer_all"] = keyP["buzzer_all"] end
    if (keyP["self_remove_odor_phase"] ~= nil) then streams["self_remove_odor_phase"] = keyP["self_remove_odor_phase"] end
    if (keyP["high_temp_remove_odor_alone"] ~= nil) then streams["high_temp_remove_odor_alone"] = keyP
        ["high_temp_remove_odor_alone"] end
    if (keyP["power_lock"] ~= nil) then if (keyP["power_lock"] == 0x00) then streams["power_lock"] = "off" elseif (keyP["power_lock"] == 0x01) then streams["power_lock"] =
            "on" end end
    if (keyP["ptc_lock"] ~= nil) then if (keyP["ptc_lock"] == 0x00) then streams["ptc_lock"] = "off" elseif (keyP["ptc_lock"] == 0x01) then streams["ptc_lock"] =
            "on" end end
    if (keyP["offline_operating_time"] ~= nil) then streams["offline_operating_time"] = keyP["offline_operating_time"] end
    if (keyP["ozone"] ~= nil) then streams["ozone"] = keyP["ozone"] end
    if (keyP["soft_warm"] ~= nil) then streams["soft_warm"] = keyP["soft_warm"] end
    if (keyP["fresh_air_parm"] ~= nil) then streams["fresh_air_parm"] = keyP["fresh_air_parm"] end
    if (keyP["rewarming_dry"] ~= nil) then streams["rewarming_dry"] = keyP["rewarming_dry"] end
    if (keyP["arom"] ~= nil) then streams["arom"] = keyP["arom"] end
    if (keyP["arom_fan_speed"] ~= nil) then streams["arom_fan_speed"] = keyP["arom_fan_speed"] end
    if (keyP["arom_time_clean"] ~= nil) then streams["arom_time_clean"] = keyP["arom_time_clean"] end
    if (keyP["arom_time"] ~= nil) then streams["arom_time"] = keyP["arom_time"] end
    if (keyP["arom_time_total"] ~= nil) then streams["arom_time_total"] = keyP["arom_time_total"] end
    if (keyP["new_mode_power"] ~= nil) then streams["new_mode_power"] = keyP["new_mode_power"] end
    if (keyP["new_temperature"] ~= nil) then streams["new_temperature"] = keyP["new_temperature"] end
    if (keyP["new_wind_speed"] ~= nil) then streams["new_wind_speed"] = keyP["new_wind_speed"] end
    if (keyP["new_mode"] ~= nil) then if (keyP["new_mode"] == 1) then streams["new_mode"] = "auto" elseif (keyP["new_mode"] == 2) then streams["new_mode"] =
            "cool" elseif (keyP["new_mode"] == 3) then streams["new_mode"] = "dry" elseif (keyP["new_mode"] == 4) then streams["new_mode"] =
            "heat" elseif (keyP["new_mode"] == 5) then streams["new_mode"] = "fan" end end
    if (keyP["uvc_remove_odor"] ~= nil) then streams["uvc_remove_odor"] = keyP["uvc_remove_odor"] end
    if (keyP["uvc_power_off"] ~= nil) then streams["uvc_power_off"] = keyP["uvc_power_off"] end
    if (keyP["main_horizontal_guide_strip_1"] ~= nil) then streams["main_horizontal_guide_strip_1"] = keyP
        ["main_horizontal_guide_strip_1"] end
    if (keyP["main_horizontal_guide_strip_2"] ~= nil) then streams["main_horizontal_guide_strip_2"] = keyP
        ["main_horizontal_guide_strip_2"] end
    if (keyP["main_horizontal_guide_strip_3"] ~= nil) then streams["main_horizontal_guide_strip_3"] = keyP
        ["main_horizontal_guide_strip_3"] end
    if (keyP["main_horizontal_guide_strip_4"] ~= nil) then streams["main_horizontal_guide_strip_4"] = keyP
        ["main_horizontal_guide_strip_4"] end
    if (keyP["has_guide_strip"] ~= nil) then streams["has_guide_strip"] = keyP["has_guide_strip"] end
    if (keyP["has_no_wind_sense"] ~= nil) then streams["has_no_wind_sense"] = keyP["has_no_wind_sense"] end
    if (keyP["light_sensitive"] ~= nil) then streams["light_sensitive"] = keyP["light_sensitive"] end
    if (keyP["has_arom"] ~= nil) then streams["has_arom"] = keyP["has_arom"] end
    if (keyP["whirl_wind_left"] ~= nil) then streams["whirl_wind_left"] = keyP["whirl_wind_left"] end
    if (keyP["whirl_wind_right"] ~= nil) then streams["whirl_wind_right"] = keyP["whirl_wind_right"] end
    if (keyP["indoor_co2"] ~= nil) then streams["indoor_co2"] = keyP["indoor_co2"] end
    if (keyP["inner_purifier"] ~= nil) then if (keyP["inner_purifier"] == 0x00) then streams["inner_purifier"] = "off" elseif (keyP["inner_purifier"] == 0x01) then streams["inner_purifier"] =
            "on" end end
    if (keyP["inner_purifier_fan_speed"] ~= nil) then streams["inner_purifier_fan_speed"] = keyP
        ["inner_purifier_fan_speed"] end
    if (keyP["inner_purifier_mode"] ~= nil) then streams["inner_purifier_mode"] = keyP["inner_purifier_mode"] end
    if (keyP["remove_odor"] ~= nil) then if (keyP["remove_odor"] == 0x00) then streams["remove_odor"] = "off" elseif (keyP["remove_odor"] == 0x01) then streams["remove_odor"] =
            "on" end end
    if (keyP["remove_odor_fan_speed"] ~= nil) then streams["remove_odor_fan_speed"] = keyP["remove_odor_fan_speed"] end
    if (keyP["fresh_air_on_co2"] ~= nil) then streams["fresh_air_on_co2"] = keyP["fresh_air_on_co2"] end
    if (keyP["fresh_air_off_co2"] ~= nil) then streams["fresh_air_off_co2"] = keyP["fresh_air_off_co2"] end
    if (keyP["linkage"] ~= nil) then streams["linkage"] = keyP["linkage"] end
    if (keyP["moisturizing"] ~= nil) then streams["moisturizing"] = keyP["moisturizing"] end
    if (keyP["moisturizing_fan_speed"] ~= nil) then streams["moisturizing_fan_speed"] = keyP["moisturizing_fan_speed"] end
    if (keyP["no_wind_sense_left"] ~= nil) then if (keyP["no_wind_sense_left"] == 0x01) then streams["no_wind_sense_left"] =
            "off" elseif (keyP["no_wind_sense_left"] == 0x02) then streams["no_wind_sense_left"] = "on" end end
    if (keyP["no_wind_sense_right"] ~= nil) then if (keyP["no_wind_sense_right"] == 0x01) then streams["no_wind_sense_right"] =
            "off" elseif (keyP["no_wind_sense_right"] == 0x02) then streams["no_wind_sense_right"] = "on" end end
    if (keyP["fresh_filter_reset"] ~= nil) then streams["fresh_filter_reset"] = keyP["fresh_filter_reset"] end
    if (keyP["five_dimension_mode"] ~= nil) then streams["five_dimension_mode"] = keyP["five_dimension_mode"] end
    if (keyP["screen_display_time"] ~= nil) then streams["screen_display_time"] = keyP["screen_display_time"] end
    if (keyP["total_status_switch"] ~= nil) then streams["total_status_switch"] = keyP["total_status_switch"] end
    if (keyP["linkage_fan_speed"] ~= nil) then streams["linkage_fan_speed"] = keyP["linkage_fan_speed"] end
    if (keyP["wind_no_linkage"] ~= nil) then streams["wind_no_linkage"] = keyP["wind_no_linkage"] end
    if (keyP["wait_clean"] ~= nil) then streams["wait_clean"] = keyP["wait_clean"] end
    if (keyP["self_clean_time"] ~= nil) then streams["self_clean_time"] = keyP["self_clean_time"] end
    if (keyP["dry_clean_time"] ~= nil) then streams["dry_clean_time"] = keyP["dry_clean_time"] end
    if (keyP["ptc_load"] ~= nil) then streams["ptc_load"] = keyP["ptc_load"] end
    if (keyP["defrosting_load"] ~= nil) then streams["defrosting_load"] = keyP["defrosting_load"] end
    if (keyP["no_wind_sense_judge_param"] ~= nil) then streams["no_wind_sense_judge_param"] = keyP
        ["no_wind_sense_judge_param"] end
    if (keyP["left_down_real_wind_speed"] ~= nil) then streams["left_down_real_wind_speed"] = keyP
        ["left_down_real_wind_speed"] end
    if (keyP["right_up_real_wind_speed"] ~= nil) then streams["right_up_real_wind_speed"] = keyP
        ["right_up_real_wind_speed"] end
    if (keyP["left_ud_wind_angle"] ~= nil) then streams["left_ud_wind_angle"] = keyP["left_ud_wind_angle"] end
    if (keyP["up_lr_wind_angle"] ~= nil) then streams["up_lr_wind_angle"] = keyP["up_lr_wind_angle"] end
    if (keyP["swing_lr_under_angle"] ~= nil) then streams["swing_lr_under_angle"] = keyP["swing_lr_under_angle"] end
    if (keyP["right_ud_wind_angle"] ~= nil) then streams["right_ud_wind_angle"] = keyP["right_ud_wind_angle"] end
    if (keyP["left_lr_wind_angle"] ~= nil) then streams["left_lr_wind_angle"] = keyP["left_lr_wind_angle"] end
    if (keyP["right_lr_wind_angle"] ~= nil) then streams["right_lr_wind_angle"] = keyP["right_lr_wind_angle"] end
    if (keyP["dry_clean_stage"] ~= nil) then streams["dry_clean_stage"] = keyP["dry_clean_stage"] end
    if (keyP["self_clean_stage"] ~= nil) then streams["self_clean_stage"] = keyP["self_clean_stage"] end
    if (keyP["real_mode"] ~= nil) then streams["real_mode"] = keyP["real_mode"] end
    if (keyP["jet_cool"] ~= nil) then if (keyP["jet_cool"] == 0x00) then streams["jet_cool"] = "off" elseif (keyP["jet_cool"] == 0x01) then streams["jet_cool"] =
            "on" end end
    if (keyP["wind_swing_ud_angle_up"] ~= nil) then streams["wind_swing_ud_angle_up"] = keyP["wind_swing_ud_angle_up"] end
    if (keyP["wind_swing_ud_angle_down"] ~= nil) then streams["wind_swing_ud_angle_down"] = keyP
        ["wind_swing_ud_angle_down"] end
    if (keyP["app_control_remember_ud"] ~= nil) then streams["app_control_remember_ud"] = keyP
        ["app_control_remember_ud"] end
    if (keyP["wind_swing_lr_angle_up"] ~= nil) then streams["wind_swing_lr_angle_up"] = keyP["wind_swing_lr_angle_up"] end
    if (keyP["wind_swing_lr_angle_down"] ~= nil) then streams["wind_swing_lr_angle_down"] = keyP
        ["wind_swing_lr_angle_down"] end
    if (keyP["app_control_remember_lr"] ~= nil) then streams["app_control_remember_lr"] = keyP
        ["app_control_remember_lr"] end
    if (keyP["has_wind_swing_ud_angle_diy"] ~= nil) then streams["has_wind_swing_ud_angle_diy"] = keyP
        ["has_wind_swing_ud_angle_diy"] end
    if (keyP["has_wind_swing_lr_angle_diy"] ~= nil) then streams["has_wind_swing_lr_angle_diy"] = keyP
        ["has_wind_swing_lr_angle_diy"] end
    if (keyP["has_left_down_real_wind_speed"] ~= nil) then streams["has_left_down_real_wind_speed"] = keyP
        ["has_left_down_real_wind_speed"] end
    if (keyP["smart_dry_value"] ~= nil) then streams["smart_dry_value"] = keyP["smart_dry_value"] end
    if (keyP["screen_display_select"] ~= nil) then streams["screen_display_select"] = keyP["screen_display_select"] end
    if (keyP["no_wind_sense_down"] ~= nil) then streams["no_wind_sense_down"] = keyP["no_wind_sense_down"] end
    if (keyP["no_wind_sense_up"] ~= nil) then streams["no_wind_sense_up"] = keyP["no_wind_sense_up"] end
    if (keyP["auto_prevent_cold_wind"] ~= nil) then streams["auto_prevent_cold_wind"] = keyP["auto_prevent_cold_wind"] end
    if (keyP["linkage_2"] ~= nil) then streams["linkage_2"] = keyP["linkage_2"] end
    if (keyP["quick_cool_heat"] ~= nil) then streams["quick_cool_heat"] = keyP["quick_cool_heat"] end
    if (keyP["has_right_ud_wind_angle"] ~= nil) then streams["has_right_ud_wind_angle"] = keyP
        ["has_right_ud_wind_angle"] end
    if (keyP["has_no_wind_sense_judge_param"] ~= nil) then streams["has_no_wind_sense_judge_param"] = keyP
        ["has_no_wind_sense_judge_param"] end
    if (keyP["cool_power_saving"] ~= nil) then streams["cool_power_saving"] = keyP["cool_power_saving"] end
    if (keyP["ieco_switch"] ~= nil) then streams["ieco_switch"] = keyP["ieco_switch"] end
    if (keyP["ieco_target_rate"] ~= nil) then streams["ieco_target_rate"] = keyP["ieco_target_rate"] end
    if (keyP["ieco_indoor_wind_speed"] ~= nil) then streams["ieco_indoor_wind_speed"] = keyP["ieco_indoor_wind_speed"] end
    if (keyP["ieco_outdoor_wind_speed"] ~= nil) then streams["ieco_outdoor_wind_speed"] = keyP
        ["ieco_outdoor_wind_speed"] end
    if (keyP["ieco_expansion_valve"] ~= nil) then streams["ieco_expansion_valve"] = keyP["ieco_expansion_valve"] end
    if (keyP["ieco_frame"] ~= nil) then streams["ieco_frame"] = keyP["ieco_frame"] end
    if (keyP["ieco_number"] ~= nil) then streams["ieco_number"] = keyP["ieco_number"] end
    if (keyP["has_ieco"] ~= nil) then streams["has_ieco"] = keyP["has_ieco"] end
    if (keyP["prepare_food"] ~= nil) then streams["prepare_food"] = keyP["prepare_food"] end
    if (keyP["quick_fry"] ~= nil) then streams["quick_fry"] = keyP["quick_fry"] end
    if (keyP["quick_fry_center_point"] ~= nil) then streams["quick_fry_center_point"] = keyP["quick_fry_center_point"] end
    if (keyP["quick_fry_angle"] ~= nil) then streams["quick_fry_angle"] = keyP["quick_fry_angle"] end
    if (keyP["prepare_food_temp"] ~= nil) then streams["prepare_food_temp"] = keyP["prepare_food_temp"] end
    if (keyP["prepare_food_fan_speed"] ~= nil) then streams["prepare_food_fan_speed"] = keyP["prepare_food_fan_speed"] end
    if (keyP["quick_fry_center_point"] ~= nil) then streams["quick_fry_center_point"] = keyP["quick_fry_center_point"] end
    if (keyP["quick_fry_angle"] ~= nil) then streams["quick_fry_angle"] = keyP["quick_fry_angle"] end
    if (keyP["care_mode"] ~= nil) then streams["care_mode"] = keyP["care_mode"] end
    if (keyP["care_mode_lock"] ~= nil) then streams["care_mode_lock"] = keyP["care_mode_lock"] end
    if (keyP["cool_light_color_r"] ~= nil) then streams["cool_light_color_r"] = keyP["cool_light_color_r"] end
    if (keyP["cool_light_color_g"] ~= nil) then streams["cool_light_color_g"] = keyP["cool_light_color_g"] end
    if (keyP["cool_light_color_b"] ~= nil) then streams["cool_light_color_b"] = keyP["cool_light_color_b"] end
    if (keyP["heat_light_color_r"] ~= nil) then streams["heat_light_color_r"] = keyP["heat_light_color_r"] end
    if (keyP["heat_light_color_g"] ~= nil) then streams["heat_light_color_g"] = keyP["heat_light_color_g"] end
    if (keyP["heat_light_color_b"] ~= nil) then streams["heat_light_color_b"] = keyP["heat_light_color_b"] end
    if (keyP["dry_light_color_r"] ~= nil) then streams["dry_light_color_r"] = keyP["dry_light_color_r"] end
    if (keyP["dry_light_color_g"] ~= nil) then streams["dry_light_color_g"] = keyP["dry_light_color_g"] end
    if (keyP["dry_light_color_b"] ~= nil) then streams["dry_light_color_b"] = keyP["dry_light_color_b"] end
    if (keyP["remove_odor_light_color_r"] ~= nil) then streams["remove_odor_light_color_r"] = keyP
        ["remove_odor_light_color_r"] end
    if (keyP["remove_odor_light_color_g"] ~= nil) then streams["remove_odor_light_color_g"] = keyP
        ["remove_odor_light_color_g"] end
    if (keyP["remove_odor_light_color_b"] ~= nil) then streams["remove_odor_light_color_b"] = keyP
        ["remove_odor_light_color_b"] end
    if (keyP["fresh_light_color_r"] ~= nil) then streams["fresh_light_color_r"] = keyP["fresh_light_color_r"] end
    if (keyP["fresh_light_color_g"] ~= nil) then streams["fresh_light_color_g"] = keyP["fresh_light_color_g"] end
    if (keyP["fresh_light_color_b"] ~= nil) then streams["fresh_light_color_b"] = keyP["fresh_light_color_b"] end
    if (keyP["purifier_light_color_r"] ~= nil) then streams["purifier_light_color_r"] = keyP["purifier_light_color_r"] end
    if (keyP["purifier_light_color_g"] ~= nil) then streams["purifier_light_color_g"] = keyP["purifier_light_color_g"] end
    if (keyP["purifier_light_color_b"] ~= nil) then streams["purifier_light_color_b"] = keyP["purifier_light_color_b"] end
    if (keyP["has_linkage_2"] ~= nil) then streams["has_linkage_2"] = keyP["has_linkage_2"] end
    if (keyP["dust_full_time_reset"] ~= nil) then streams["dust_full_time_reset"] = keyP["dust_full_time_reset"] end
    if (keyP["circle_fan"] ~= nil) then streams["circle_fan"] = keyP["circle_fan"] end
    if (keyP["circle_fan_mode"] ~= nil) then streams["circle_fan_mode"] = keyP["circle_fan_mode"] end
    if (keyP["linkage_2_fresh_air_auto"] ~= nil) then streams["linkage_2_fresh_air_auto"] = keyP
        ["linkage_2_fresh_air_auto"] end
    if (keyP["linkage_2_humi_auto"] ~= nil) then streams["linkage_2_humi_auto"] = keyP["linkage_2_humi_auto"] end
    if (keyP["linkage_2_purifier_auto"] ~= nil) then streams["linkage_2_purifier_auto"] = keyP
        ["linkage_2_purifier_auto"] end
    if (keyP["linkage_2_temp_auto"] ~= nil) then streams["linkage_2_temp_auto"] = keyP["linkage_2_temp_auto"] end
    if (keyP["linkage_2_wind_auto"] ~= nil) then streams["linkage_2_wind_auto"] = keyP["linkage_2_wind_auto"] end
    if (keyP["breath_cool"] ~= nil) then streams["breath_cool"] = keyP["breath_cool"] end
    if (keyP["breath_fresh_air"] ~= nil) then streams["breath_fresh_air"] = keyP["breath_fresh_air"] end
    if (keyP["breath_heat"] ~= nil) then streams["breath_heat"] = keyP["breath_heat"] end
    if (keyP["breath_purifier"] ~= nil) then streams["breath_purifier"] = keyP["breath_purifier"] end
    if (keyP["breath_remove_odor"] ~= nil) then streams["breath_remove_odor"] = keyP["breath_remove_odor"] end
    if (keyP["prevent_straight_wind_distance"] ~= nil) then streams["prevent_straight_wind_distance"] = keyP
        ["prevent_straight_wind_distance"] end
    if (keyP["auto_prevent_cold_wind_memory"] ~= nil) then streams["auto_prevent_cold_wind_memory"] = keyP
        ["auto_prevent_cold_wind_memory"] end
    if (keyP["has_auto_prevent_cold_wind_memory"] ~= nil) then streams["has_auto_prevent_cold_wind_memory"] = keyP
        ["has_auto_prevent_cold_wind_memory"] end
    if (keyP["buzzer_off_status"] ~= nil) then streams["buzzer_off_status"] = keyP["buzzer_off_status"] end
    if (keyP["air_remove_odor"] ~= nil) then streams["air_remove_odor"] = keyP["air_remove_odor"] end
    if (keyP["has_moisturizing"] ~= nil) then streams["has_moisturizing"] = keyP["has_moisturizing"] end
    if (keyP["eco_time_hour"] ~= nil) then streams["eco_time_hour"] = keyP["eco_time_hour"] end
    if (keyP["eco_time_min"] ~= nil) then streams["eco_time_min"] = keyP["eco_time_min"] end
    if (keyP["eco_time_sec"] ~= nil) then streams["eco_time_sec"] = keyP["eco_time_sec"] end
    if (keyP["eco_time_switch"] ~= nil) then streams["eco_time_switch"] = keyP["eco_time_switch"] end
    if (keyP["clean_breath"] ~= nil) then streams["clean_breath"] = keyP["clean_breath"] end
    if (keyP["clean_breath_level"] ~= nil) then streams["clean_breath_level"] = keyP["clean_breath_level"] end
    if (keyP["remove_odor_time"] ~= nil) then streams["remove_odor_time"] = keyP["remove_odor_time"] end
    if (keyP["tvoc_level"] ~= nil) then streams["tvoc_level"] = keyP["tvoc_level"] end
    if (keyP["health"] ~= nil) then streams["health"] = keyP["health"] end
    if (keyP["arofene_filter_use_time"] ~= nil) then streams["arofene_filter_use_time"] = keyP
        ["arofene_filter_use_time"] end
    if (keyP["tvoc_density"] ~= nil) then streams["tvoc_density"] = keyP["tvoc_density"] end
    if (keyP["strong_cool"] ~= nil) then streams["strong_cool"] = keyP["strong_cool"] end
    if (keyP["has_strong_cool"] ~= nil) then streams["has_strong_cool"] = keyP["has_strong_cool"] end
    if (keyP["humidification"] ~= nil) then streams["humidification"] = keyP["humidification"] end
    if (keyP["humidification_fan_speed"] ~= nil) then streams["humidification_fan_speed"] = keyP
        ["humidification_fan_speed"] end
    if (keyP["humidification_mode"] ~= nil) then streams["humidification_mode"] = keyP["humidification_mode"] end
    if (keyP["has_humidification"] ~= nil) then streams["has_humidification"] = keyP["has_humidification"] end
    keyP["propertyNumber"] = 0
    keyP["prevent_super_cool"] = nil
    keyP["prevent_straight_wind"] = nil
    keyP["auto_prevent_straight_wind"] = nil
    keyP["wind_straight"] = nil
    keyP["wind_avoid"] = nil
    keyP["yb_wind_avoid"] = nil
    keyP["intelligent_wind"] = nil
    keyP["self_clean"] = nil
    keyP["no_wind_sense"] = nil
    keyP["no_wind_sense_level"] = nil
    keyP["fn_no_wind_sense"] = nil
    keyP["child_prevent_cold_wind"] = nil
    keyP["little_angel"] = nil
    keyP["cool_hot_sense"] = nil
    keyP["gentle_wind_sense"] = nil
    keyP["prevent_straight_wind_fa"] = nil
    keyP["no_wind_sense_fa"] = nil
    keyP["security"] = nil
    keyP["even_wind"] = nil
    keyP["single_tuyere"] = nil
    keyP["extreme_wind"] = nil
    keyP["extreme_wind_level"] = nil
    keyP["voice_control"] = nil
    keyP["pre_cool_hot"] = nil
    keyP["water_washing"] = nil
    keyP["fresh_air"] = nil
    keyP["fa_prevent_straight_wind"] = nil
    keyP["parent_control"] = nil
    keyP["parent_control_temp_up"] = nil
    keyP["parent_control_temp_down"] = nil
    keyP["nobody_energy_save"] = nil
    keyP["filter_value"] = nil
    keyP["filter_level"] = nil
    keyP["prevent_straight_wind_lr"] = nil
    keyP["pm25_value"] = nil
    keyP["water_pump"] = nil
    keyP["intelligent_control"] = nil
    keyP["volume_control"] = nil
    keyP["voice_control_new"] = nil
    keyP["wind_swing_ud_angle"] = nil
    keyP["wind_swing_lr_angle"] = nil
    keyP["face_register"] = nil
    keyP["cool_temp_up"] = nil
    keyP["cool_temp_down"] = nil
    keyP["auto_temp_up"] = nil
    keyP["auto_temp_down"] = nil
    keyP["heat_temp_up"] = nil
    keyP["heat_temp_down"] = nil
    keyP["remote_control_lock"] = nil
    keyP["remote_control_lock_control"] = nil
    keyP["operating_time"] = nil
    -- keyP["indoor_humidity"] = nil  -- preserve C1/0x45 value across messages
    keyP["degerming"] = nil
    keyP["light"] = nil
    keyP["wind_top"] = nil
    keyP["wind_around"] = nil
    keyP["wind_around_ud"] = nil
    keyP["child_lock"] = nil
    keyP["is_query"] = nil
    keyP["analysis_value"] = nil
    keyP["filter_replace_time"] = nil
    keyP["dust_full_time"] = nil
    keyP["buzzer_all"] = nil
    keyP["self_remove_odor_phase"] = nil
    keyP["high_temp_remove_odor_alone"] = nil
    keyP["power_lock"] = nil
    keyP["ptc_lock"] = nil
    keyP["offline_operating_time"] = nil
    keyP["ozone"] = nil
    keyP["fault_tag"] = nil
    keyP["soft_warm"] = nil
    keyP["fresh_air_parm"] = nil
    keyP["rewarming_dry"] = nil
    keyP["arom"] = nil
    keyP["arom_old"] = nil
    keyP["arom_fan_speed"] = nil
    keyP["arom_time_clean"] = nil
    keyP["arom_time"] = nil
    keyP["arom_time_total"] = nil
    keyP["new_mode_power"] = nil
    keyP["new_mode"] = nil
    keyP["new_temperature"] = nil
    keyP["new_wind_speed"] = nil
    keyP["uvc_remove_odor"] = nil
    keyP["uvc_power_off"] = nil
    keyP["main_horizontal_guide_strip_1"] = nil
    keyP["main_horizontal_guide_strip_2"] = nil
    keyP["main_horizontal_guide_strip_3"] = nil
    keyP["main_horizontal_guide_strip_4"] = nil
    keyP["has_guide_strip"] = nil
    keyP["has_no_wind_sense"] = nil
    keyP["light_sensitive"] = nil
    keyP["has_arom"] = nil
    keyP["t2_temp"] = nil
    keyP["whirl_wind_left"] = nil
    keyP["whirl_wind_right"] = nil
    keyP["inner_purifier"] = nil
    keyP["inner_purifier_fan_speed"] = nil
    keyP["inner_purifier_mode"] = nil
    keyP["fresh_air_mode_two"] = nil
    keyP["wind_speed_right"] = nil
    keyP["indoor_co2"] = nil
    keyP["humidification"] = nil
    keyP["humidification_fan_speed"] = nil
    keyP["humidification_mode"] = nil
    keyP["remove_odor"] = nil
    keyP["remove_odor_fan_speed"] = nil
    keyP["fresh_air_on_co2"] = nil
    keyP["fresh_air_off_co2"] = nil
    keyP["gentle_wind_enable"] = nil
    keyP["linkage"] = nil
    keyP["moisturizing"] = nil
    keyP["moisturizing_fan_speed"] = nil
    keyP["no_wind_sense_left"] = nil
    keyP["no_wind_sense_right"] = nil
    keyP["no_wind_sense_control"] = nil
    tempControl = 0
    keyP["is_query"] = nil
    keyP["timerSignal"] = 0
    keyP["powerValue"] = nil
    keyP["modeValue"] = nil
    keyP["smartDryValue"] = nil
    keyP["temperature"] = nil
    keyP["smallTemperature"] = nil
    keyP["indoorTemperatureValue"] = nil
    keyP["smallIndoorTemperatureValue"] = nil
    keyP["outdoorTemperatureValue"] = nil
    keyP["smallOutdoorTemperatureValue"] = nil
    keyP["fanspeedValue"] = nil
    keyP["closeTimerSwitch"] = nil
    keyP["openTimerSwitch"] = nil
    keyP["closeHour"] = nil
    keyP["closeStepMintues"] = nil
    keyP["closeMin"] = nil
    keyP["closeTime"] = nil
    keyP["openHour"] = nil
    keyP["openStepMintues"] = nil
    keyP["openMin"] = nil
    keyP["openTime"] = nil
    keyP["strongWindValue"] = nil
    keyP["comfortableSleepValue"] = nil
    keyP["comfortableSleepSwitch"] = nil
    keyP["comfortableSleepTime"] = nil
    keyP["comfort_sleep_curve"] = nil
    keyP["PTCValue"] = nil
    keyP["purifierValue"] = nil
    keyP["ecoValue"] = nil
    keyP["dryValue"] = nil
    keyP["swingLRValue"] = nil
    keyP["swingUDValue"] = nil
    keyP["swingLRValueUnder"] = nil
    keyP["swingLRUnderSwitch"] = 0
    keyP["currentWorkTime"] = nil
    keyP["PTCForceValue"] = 0
    keyP["screenDisplayNowValue"] = nil
    keyP["wind_swing_ud_right"] = nil
    keyP["wind_swing_lr_right"] = nil
    keyP["wind_swing_lr_left"] = nil
    keyP["wind_swing_ud_left"] = nil
    keyP["linkage_sync"] = nil
    keyP["screen_display"] = nil
    keyP["ptc_default_rule"] = nil
    keyP["fresh_filter_reset"] = nil
    keyP["comfortPowerSave"] = nil
    keyP["five_dimension_mode"] = nil
    keyP["screen_display_time"] = nil
    keyP["total_status_switch"] = nil
    keyP["linkage_fan_speed"] = nil
    keyP["wind_no_linkage"] = nil
    keyP["wait_clean"] = nil
    keyP["self_clean_time"] = nil
    keyP["self_clean_stage"] = nil
    keyP["dry_clean_time"] = nil
    keyP["dry_clean_stage"] = nil
    keyP["ptc_load"] = nil
    keyP["defrosting_load"] = nil
    keyP["no_wind_sense_judge_param"] = nil
    keyP["left_down_real_wind_speed"] = nil
    keyP["right_up_real_wind_speed"] = nil
    keyP["left_ud_wind_angle"] = nil
    keyP["up_lr_wind_angle"] = nil
    keyP["swing_lr_under_angle"] = nil
    keyP["right_ud_wind_angle"] = nil
    keyP["left_lr_wind_angle"] = nil
    keyP["right_lr_wind_angle"] = nil
    keyP["real_mode"] = nil
    keyP["jet_cool"] = nil
    keyP["wind_swing_ud_angle_up"] = nil
    keyP["wind_swing_ud_angle_down"] = nil
    keyP["app_control_remember_ud"] = nil
    keyP["wind_swing_lr_angle_up"] = nil
    keyP["wind_swing_lr_angle_down"] = nil
    keyP["app_control_remember_lr"] = nil
    keyP["has_left_down_real_wind_speed"] = nil
    keyP["smart_dry_value"] = nil
    keyP["screen_display_select"] = nil
    keyP["wind_swing_lr_under"] = nil
    keyP["no_wind_sense_down"] = nil
    keyP["no_wind_sense_up"] = nil
    keyP["no_wind_sense_updown_control"] = nil
    keyP["auto_prevent_cold_wind"] = nil
    keyP["linkage_2"] = nil
    keyP["cool_power_saving"] = nil
    keyP["has_no_wind_sense_judge_param"] = nil
    keyP["has_right_ud_wind_angle"] = nil
    keyP["ieco_switch"] = nil
    keyP["ieco_target_rate"] = nil
    keyP["ieco_indoor_wind_speed"] = nil
    keyP["ieco_outdoor_wind_speed"] = nil
    keyP["ieco_expansion_valve"] = nil
    keyP["ieco_frame"] = nil
    keyP["ieco_number"] = nil
    keyP["quick_cool_heat"] = nil
    keyP["prepare_food"] = nil
    keyP["prepare_food_temp"] = nil
    keyP["prepare_food_fan_speed"] = nil
    keyP["quick_fry"] = nil
    keyP["quick_fry_temp"] = nil
    keyP["quick_fry_fan_speed"] = nil
    keyP["quick_fry_center_point"] = nil
    keyP["quick_fry_angle"] = nil
    keyP["quick_fry_control"] = nil
    keyP["light_color_control"] = nil
    keyP["care_mode"] = nil
    keyP["care_mode_lock"] = nil
    keyP["has_linkage_2"] = nil
    keyP["dust_full_time_reset"] = nil
    keyP["circle_fan"] = nil
    keyP["circle_fan_mode"] = nil
    keyP["power_saving"] = nil
    keyP["linkage_2_temp_auto"] = nil
    keyP["linkage_2_wind_auto"] = nil
    keyP["linkage_2_fresh_air_auto"] = nil
    keyP["linkage_2_purifier_auto"] = nil
    keyP["linkage_2_humi_auto"] = nil
    keyP["linkage_2_temp_control_type"] = nil
    keyP["linkage_2_wind_control_type"] = nil
    keyP["linkage_2_fresh_air_control_type"] = nil
    keyP["linkage_2_purifier_control_type"] = nil
    keyP["linkage_2_humi_control_type"] = nil
    keyP["breath_cool"] = nil
    keyP["breath_fresh_air"] = nil
    keyP["breath_heat"] = nil
    keyP["breath_purifier"] = nil
    keyP["breath_remove_odor"] = nil
    keyP["prevent_straight_wind_distance"] = nil
    keyP["auto_prevent_cold_wind_memory"] = nil
    keyP["buzzer_off_status"] = nil
    keyP["air_remove_odor"] = nil
    keyP["has_moisturizing"] = nil
    keyP["clean_breath"] = nil
    keyP["clean_breath_level"] = nil
    keyP["remove_odor_fan_speed"] = nil
    keyP["remove_odor_time"] = nil
    keyP["tvoc_level"] = nil
    keyP["health"] = nil
    keyP["remove_arofene_clean"] = nil
    keyP["control_source"] = nil
    keyP["tvoc_density"] = nil
    keyP["arofene_filter_use_time"] = nil
    keyP["strong_cool"] = nil
    keyP["has_strong_cool"] = nil
    local retTable = {}
    retTable["status"] = streams
    local ret = encode(retTable)
    return ret
end
