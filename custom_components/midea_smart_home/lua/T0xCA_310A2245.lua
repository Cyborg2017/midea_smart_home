local bit = require "bit".bit
local JSON = require "cjson"
local uptable = {}
uptable["KEY_VERSION"] = "version"
uptable["VALUE_VERSION"] = "66"
uptable["BYTE_DEVICE_TYPE"] = 0xCA
uptable["BYTE_MSG_TYPE_CONTROL"] = 0x02
uptable["BYTE_MSG_TYPE_QUERY"] = 0x03
uptable["BYTE_PROTOCOL_HEAD"] = 0xAA
uptable["BYTE_PROTOCOL_HEAD_LENGTH"] = 0x0A
uptable["codeMode"] = 0
uptable["freezingMode"] = 0
uptable["smartMode"] = 0
uptable["energySavingMode"] = 0
uptable["holidayMode"] = 0
uptable["moisturizeMode"] = 0
uptable["preservationMode"] = 0
uptable["acmeFreezingMode"] = 0
uptable["refrigerationPowerValue"] = 0
uptable["lVariablePowerValue"] = 0
uptable["rVariablePowerValue"] = 0
uptable["freezingPowerValue"] = 0
uptable["crossPeakElectricity"] = 0
uptable["allRefrigerationPower"] = 0
uptable["refrigerationTemperature"] = 0
uptable["freezingTemperature"] = 0
uptable["lVariableTemperature"] = 0
uptable["rVariableTemperature"] = 0
uptable["variableModeValue"] = 0
uptable["removeDew"] = 0
uptable["humidify"] = 0
uptable["unfreeze"] = 0
uptable["temperatureUnit"] = 0
uptable["floodlight"] = 0
uptable["functionSwitch"] = 0
uptable["radarMode"] = 0
uptable["milkMode"] = 0
uptable["icedMode"] = 0
uptable["plasmaAsepticMode"] = 0
uptable["acquireIceaMode"] = 0
uptable["brashIceaMode"] = 0
uptable["acquireWaterMode"] = 0
uptable["freezingIceMachinePower"] = 0
uptable["freezingFahrenheit"] = 0
uptable["refrigerationFahrenheit"] = 0
uptable["leachExpireDay"] = 0
uptable["powerConsumptionLow"] = 0
uptable["powerConsumptionHigh"] = 0
uptable["freezingMotorResetStatus"] = 0
uptable["freezingMotorDeicingStatus"] = 0
uptable["freezingIceMachineWaterStatus"] = 0
uptable["freezingAllIceStatus"] = 0
uptable["humanInduction"] = 0
uptable["humanInductionLightSwitch"] = 0
uptable["refrigerationDoorPower"] = 0
uptable["freezingDoorPower"] = 0
uptable["variableDoorPower"] = 0
uptable["storageIceHomeDoorState"] = 0
uptable["purineInhibitDrawerSwitch"] = 0
uptable["barDoorPower"] = 0
uptable["iceMouthPower"] = 0
uptable["isError"] = 0
uptable["intervalRoomHumidityLevel"] = 0
uptable["refrigerationRealTemperature"] = 0
uptable["freezingRealTemperature"] = 0
uptable["lVariableRealTemperature"] = 0
uptable["rVariableRealTemperature"] = 0
uptable["fastColdMinuteLow"] = 0
uptable["fastColdMinuteHigh"] = 0
uptable["fastFreezeMinuteLow"] = 0
uptable["fastFreezeMinuteHigh"] = 0
uptable["foodSite"] = 0
uptable["beef"] = 0
uptable["pork"] = 0
uptable["mutton"] = 0
uptable["chicken"] = 0
uptable["duckMeat"] = 0
uptable["fish"] = 0
uptable["shrimp"] = 0
uptable["dumplings"] = 0
uptable["gluePudding"] = 0
uptable["iceCream"] = 0
uptable["microcrystalFresh"] = 0
uptable["dryZone"] = 0
uptable["electronicSmell"] = 0
uptable["eradicatePesticideResidue"] = 0
uptable["eradicatePesticideResidueProgress"] = 0
uptable["eradicatePesticideResidueCompletion"] = 0
uptable["humidity"] = 0
uptable["storageModeCompletion"] = 0
uptable["freezingModeCompletion"] = 0
uptable["humidifierWaterShortage"] = 0
uptable["plasmaAsepticCompletion"] = 0
uptable["acmeFreezingCompletion"] = 0
uptable["performanceMode"] = 0
uptable["normalTemperatureLevel"] = 0
uptable["functionZoneLevel"] = 0
uptable["humiditySetting"] = 0
uptable["smartHumidity"] = 0
uptable["storageLeftDoorAuto"] = 0
uptable["storageRightDoorAuto"] = 0
uptable["freezerDoorAuto"] = 0
uptable["freezerDoorAutoControl"] = 0
uptable["storageDoorAutoControl"] = 0
uptable["flexDoorAuto"] = 0
uptable["freezerDownDoorAuto"] = 0
uptable["storageIceMachinePower"] = 0
uptable["storageMotorResetStatus"] = 0
uptable["storageMotorDeicingStatus"] = 0
uptable["storageIceMachineWaterStatus"] = 0
uptable["storageAllIceStatus"] = 0
uptable["filterExpiresMildWarning"] = 0
uptable["filterExpiresSevereWarning"] = 0
uptable["filterReplacementWarningElimination"] = 0
uptable["iceRoomRealTemperature"] = 0
uptable["storageFTemperature"] = 0
uptable["freezingFTemperature"] = 0
uptable["leftFlexzoneFTemperature"] = 0
uptable["electronicCleanStrong"] = 0
uptable["electronicCleanTimeout"] = 0
uptable["quickBeverageTime"] = 0
uptable["quickBeverage"] = 0
uptable["quickBeverageCompletion"] = 0
uptable["dataType"] = 0
uptable["storageDoorOpenOvertime"] = 0
uptable["freezerDoorOpenOvertime"] = 0
uptable["barDoorOpenOvertime"] = 0
uptable["variableDoorOpenOvertime"] = 0
uptable["iceMachineFull"] = 0
uptable["refrigerationSensorError"] = 0
uptable["refrigerationDefrostingSensorError"] = 0
uptable["ringTemperatureSensorError"] = 0
uptable["flexzoneSensorError"] = 0
uptable["rightFlexzoneSensorError"] = 0
uptable["freezingHighTemperature"] = 0
uptable["freezingSensorError"] = 0
uptable["freezingDefrostingSensorError"] = 0
uptable["iceElectricalMachineryError"] = 0
uptable["refrigerationDefrostingOvertime"] = 0
uptable["freezingDefrostingOvertime"] = 0
uptable["zeroCrossingCheckError"] = 0
uptable["eepromReadWriteError"] = 0
uptable["leftFlexzoneSensorError"] = 0
uptable["iceRoomSensorError"] = 0
uptable["mainDisplayCorrespondError"] = 0
uptable["iceMachineTemperatureError"] = 0
uptable["flexzoneDefrostingSensorError"] = 0
uptable["flexzoneDefrostingSensor2Error"] = 0
uptable["yogurtMachineSensorError"] = 0
uptable["iceMachineFrettingSwitchError"] = 0
uptable["iceMachinePipeFilterOvertime"] = 0
uptable["ambientHumiditySensorError"] = 0
uptable["storageHumiditySensorError"] = 0
uptable["radarSensor1Error"] = 0
uptable["radarSensor2Error"] = 0
uptable["radarSensor3Error"] = 0
uptable["radarSensor4Error"] = 0
uptable["radarSensor5Error"] = 0
uptable["functionZoneTemperatureSensorError"] = 0
uptable["normalZoneTemperatureSensorError"] = 0
uptable["humidityControlSensorError"] = 0
uptable["openDoorTooFrequently"] = 0
uptable["storageDoorAloneOpenFrequently"] = 0
uptable["freezingDoorAloneOpenFrequently"] = 0
uptable["barDoorAloneOpenFrequently"] = 0
uptable["snWritingError"] = 0
uptable["storageTemperatureOverheating"] = 0
uptable["storageTemperatureTooLow"] = 0
uptable["storageHeatingWireSensorError"] = 0
uptable["uartReceiverError"] = 0
uptable["crystalliteMainSensorError"] = 0
uptable["crystalliteBase1SensorError"] = 0
uptable["crystalliteBase2SensorError"] = 0
uptable["crystalliteBase3SensorError"] = 0
uptable["crystalliteBase4SensorError"] = 0
uptable["iceRoomDoorOpenOvertime"] = 0
uptable["storageIceFullTips"] = 0
uptable["iceMachineSensorError"] = 0
uptable["storageIceMachineSensorError"] = 0
uptable["storageIceOperationError"] = 0
uptable["freezingIceOperationError"] = 0
uptable["mcuIceCommunicationError"] = 0
uptable["mcuFiveCommunicationError"] = 0
uptable["fiveTslCommunicationError"] = 0
uptable["twoTslCommunicationError"] = 0
uptable["fiveNOError"] = 0
uptable["fiveCTError"] = 0
uptable["aquaticProduct"] = 0
uptable["storageLightLevel"] = 0
uptable["voiceDoorAuto"] = 0
uptable["touchDoorAuto"] = 0
uptable["helpDoorAuto"] = 0
uptable["speedDoorOpen"] = 0
uptable["angleDoorOpen"] = 0
uptable["voiceAssistant"] = 0
uptable["blueRayMode"] = 0
uptable["noActionDoorClose"] = 0
uptable["foodExpireLight"] = 0
uptable["levelMsgLight"] = 0
uptable["quickIceMode"] = 0
uptable["noActionDoorCloseTime"] = 0
uptable["silentNightMode"] = 0
uptable["silentMode"] = 0
uptable["leachExpireDayHigh"] = 0
uptable["waterFlowPercentage"] = 0
uptable["crossPeakElectricityEnter"] = 0
uptable["beverageVialNumber"] = 0
uptable["beverageMidNumber"] = 0
uptable["beverageBigNumber"] = 0
uptable["beverageQuickTime"] = 0
uptable["nightMode"] = 0
uptable["quickBeverageCompleted"] = 0
uptable["localTimeHour"] = 0
uptable["localTimeMinute"] = 0
uptable["localTimeSecond"] = 0
uptable["timeZone"] = 0
uptable["week"] = 0
uptable["day"] = 0
uptable["month"] = 0
uptable["year"] = 0
uptable["eCleaningPercentage"] = 0
uptable["standbyMode"] = 0
uptable["deepColdMode"] = 0
uptable["lightingEffect"] = 0
uptable["lightingColor"] = 0
uptable["customColorR"] = 0
uptable["customColorG"] = 0
uptable["customColorB"] = 0
uptable["turnOffLight"] = 0
uptable["lightBrightness"] = 0
uptable["sunnyForSevenDays"] = 0
uptable["teslaHandleSwitchMode"] = 0
uptable["fivePreservationMode"] = 0
uptable["deliveryMode"] = 0
uptable["controlSugarFlag"] = 0
uptable["strongControlSugarFlag"] = 0
uptable["controlSugarTimeLow"] = 0
uptable["controlSugarTimeHigh"] = 0
uptable["filterNaturalTimeHigh"] = 0
uptable["filterNaturalTimeLow"] = 0
uptable["drinkValveEqualOpenHigh"] = 0
uptable["drinkValveEqualOpenLow"] = 0
uptable["inletValveEqualOpenHigh"] = 0
uptable["inletValveEqualOpenLow"] = 0
uptable["filterElementUsePercentage"] = 0
uptable["iceMakerTimesHigh"] = 0
uptable["iceMakerTimesLow"] = 0
uptable["nightLightSwitch"] = 0
uptable["handleReturnTime"] = 0
uptable["openDoorTipsSwitch"] = 0
uptable["pulseSwitch"] = 0
uptable["iceClean"] = 0
uptable["telstarSavingMode"] = 0
uptable["panelDisplayGear"] = 0
uptable["coolingTimeStartHour"] = 0
uptable["coolingTimeStartMinutes"] = 0
uptable["riseTimeStartHour"] = 0
uptable["riseTimeStartMinutes"] = 0
uptable["storageLeftDoorAutoOpenAngle"] = 0
uptable["storageRightDoorAutoOpenAngle"] = 0
uptable["globalFlexTemperature"] = 0
uptable["quickFreezing"] = 0
uptable["freezingLightOpen"] = 0
uptable["storageGlassDoorLight"] = 0
uptable["storageGlassDoorLightOpen"] = 0
uptable["vegetableFreezing"] = 0
uptable["vegetableFreezingDry"] = 0
uptable["storageDoorAutoOpen"] = 0
uptable["freezingLightOpenChose"] = 0
uptable["storageLightOpenChose"] = 0
uptable["tapTap"] = 0
uptable["wineType"] = 0
uptable["ledPwmDuty"] = 0
uptable["sleepMode"] = 0
uptable["sleepModeStartHour"] = 0
uptable["sleepModeStartMinute"] = 0
uptable["sleepModeEndHour"] = 0
uptable["sleepModeEndMinute"] = 0
uptable["iceWaterMode"] = 0
uptable["smartRecommend"] = 0
uptable["autoFill"] = 0
uptable["iceWaterMixType"] = 0
uptable["iceWaterMixProportion"] = 0
uptable["smartMorningStartHour"] = 0
uptable["iceWaterMixTypeMorning"] = 0
uptable["iceWaterMixProportionMorning"] = 0
uptable["isMorningMode"] = 0
uptable["smartNoonStartHour"] = 0
uptable["iceWaterMixTypeNoon"] = 0
uptable["iceWaterMixProportionNoon"] = 0
uptable["isNoonMode"] = 0
uptable["smartNightStartHour"] = 0
uptable["iceWaterMixTypeNight"] = 0
uptable["iceWaterMixProportionNight"] = 0
uptable["isNightMode"] = 0
uptable["waterBoxStatus"] = 0
uptable["overflowSensor"] = 0
uptable["aiFruitDisplayControl"] = 0
uptable["aiFruitFlag"] = 0
uptable["aiPurineDisplayControl"] = 0
uptable["aiPurineFlag"] = 0
uptable["aiFruitBoxGear"] = 0
uptable["offlineVoiceSwitch"] = 0
uptable["offlineVoiceSensitivity"] = 0
uptable["openDoorWarningTime"] = 12
uptable["openDoorHoverTime"] = 0
uptable["cameraSwitch"] = 0
uptable["gpsReportSwitch"] = 0
uptable["roomLedDimmingFlag"] = 0
uptable["iceMachineStopIceFlag"] = 0
uptable["displayBoardMuteFlag"] = 0
uptable["freezerLightOneMinuteFlag"] = 0
uptable["isHaveFreezingIce"] = 0
uptable["appSmartSelectionMode"] = 0
uptable["smartSelectionSetTemp"] = 0
uptable["fridgeConstantTempHumidity"] = 0
uptable["tmfCoolFreezeMode"] = 0
uptable["smartSelectionGearChange"] = 0
uptable["electronicCleanSmartMode"] = 0
uptable["freezerIcemakerWaterShortage"] = 0
uptable["freezerWaterShortageAlarm"] = 0
uptable["smartFreezeMode"] = 0
uptable["smartCoolMode"] = 0
uptable["sabbathExitTime"] = 24
uptable["sabbathMode"] = 0
uptable["multiFuncZoneStatus"] = 0
uptable["nfcSignalBoardEnabled"] = 0
uptable["nfcSignalBoardState"] = 0
uptable["defrostModeSwitch"] = 0
uptable["defrostCompletedState"] = 0
uptable["defrostRemainTime"] = 0
uptable["defrostRemainTimeData110"] = 0
uptable["defrostRemainTimeData111"] = 0
uptable["defrostTimeUserDefined"] = 0
uptable["smartAiToSelfSelect"] = 0
uptable["aiPurine2ndEstimate"] = 0
uptable["hexLength"] = 0
uptable["dividerSupportAutoFill"] = 0
uptable["foodClipData116"] = 0
uptable["foodClipData117"] = 0
uptable["wifiHumanInductionValue"] = 0
uptable["wifiHumanInductionFarValue"] = 0
uptable["wifiHumanInductionExistValue"] = 0
uptable["rangeTrackingShortValue"] = 0
uptable["rangeTrackingFarValue"] = 0
uptable["resistSpectrumSymmetryDisturbRatio"] = 0
uptable["resistSpectrumSymmetryDisturbNum"] = 0
uptable["aiHumanInductionSimilarityValue"] = 0
uptable["vacuumMode"] = 0
uptable["vacuumCompleted"] = 0
uptable["surfaceLightModeSelect"] = 0
uptable["atmosphereLampModeSelect"] = 0
uptable["handleAtmosphereLampBrightness"] = 0
uptable["colmoCoolFreezeMode"] = 0
uptable["basicPowerSavingSwitch"] = 0
uptable["powerSavingStarVersion"] = 0
uptable["delayDefrostSwitch"] = 0
uptable["demandResponseSwitch"] = 0
uptable["temporaryDeloadingSwitch"] = 0
uptable["iceClean"] = 0
uptable["deloadingMaximumExitTime"] = 0
uptable["defrostMaximumExitTime"] = 0
uptable["demandResponseMaximumExitTime"] = 0
uptable["offPeakDefrostSwitch"] = 0
uptable["coolThresholdUpwardValue"] = 0
uptable["freezeThresholdUpwardValue"] = 0
uptable["internalDeloadingMaximumExitTime"] = 0
uptable["humanSensingTriggerState"] = 0
uptable["smartDenoiseOpenHours"] = 0
uptable["smartDenoiseOpenMins"] = 0
uptable["freezerElecPowerfulDeodorizeSwitch"] = 0
uptable["freezerElecPowerfulDeodorizeHourTime"] = 0
uptable["freezerElecPowerfulDeodorizeMinTime"] = 0
uptable["storageElecPowerfulDeodorizeHourTime"] = 0
uptable["isTemperatureQuery"] = false
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
local function string2Int(data)
    if (not data) then data = tonumber("0") end
    data = tonumber(data)
    if (data == nil) then data = 0 end
    return data
end
local function int2String(data)
    if (not data) then data = tostring(0) end
    data = tostring(data)
    if (data == nil) then data = "0" end
    return data
end
local function table2string(cmd)
    local ret = ""
    local i
    for i = 1, #cmd do ret = ret .. string.char(cmd[i]) end
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
    for si = start_pos, end_pos do resVal = resVal + tmpbuf[si] end
    resVal = bit.bnot(resVal) + 1
    resVal = bit.band(resVal, 0x00ff)
    return resVal
end
local crc8_854_table = { 0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65, 157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220, 35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98, 190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255, 70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7, 219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154, 101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36, 248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185, 140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205, 17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80, 175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238, 50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115, 202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139, 87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22, 233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168, 116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53 }
local function crc8_854(dataBuf, start_pos, end_pos)
    local crc = 0
    for si = start_pos, end_pos do crc = crc8_854_table[bit.band(bit.bxor(crc, dataBuf[si]), 0xFF) + 1] end
    return crc
end
local function getTotalMsg(bodyData, cType)
    local bodyLength = #bodyData
    local msgLength = bodyLength + uptable["BYTE_PROTOCOL_HEAD_LENGTH"] + 1
    local msgBytes = {}
    for i = 0, msgLength do msgBytes[i] = 0 end
    msgBytes[0] = uptable["BYTE_PROTOCOL_HEAD"]
    msgBytes[1] = bodyLength + uptable["BYTE_PROTOCOL_HEAD_LENGTH"] + 1
    msgBytes[2] = uptable["BYTE_DEVICE_TYPE"]
    msgBytes[3] = bit.bxor((bodyLength + uptable["BYTE_PROTOCOL_HEAD_LENGTH"] + 1), uptable["BYTE_DEVICE_TYPE"])
    msgBytes[9] = cType
    for i = 0, bodyLength do msgBytes[i + uptable["BYTE_PROTOCOL_HEAD_LENGTH"]] = bodyData[i] end
    msgBytes[msgLength] = makeSum(msgBytes, 1, msgLength - 1)
    local msgFinal = {}
    for i = 1, msgLength + 1 do msgFinal[i] = msgBytes[i - 1] end
    return msgFinal
end
local function jsonToModel(jsonCmd)
    local streams = jsonCmd
    if (streams["storage_mode"] == "on") then uptable["codeMode"] = 0x01 elseif (streams["storage_mode"] == "off") then uptable["codeMode"] = 0x00 end
    if (streams["freezing_mode"] == "on") then uptable["freezingMode"] = 0x02 elseif (streams["freezing_mode"] == "off") then uptable["freezingMode"] = 0x00 end
    if (streams["intelligent_mode"] == "on") then uptable["smartMode"] = 0x04 elseif (streams["intelligent_mode"] == "off") then uptable["smartMode"] = 0x00 end
    if (streams["energy_saving_mode"] == "on") then uptable["energySavingMode"] = 0x08 elseif (streams["energy_saving_mode"] == "off") then uptable["energySavingMode"] = 0x00 end
    if (streams["holiday_mode"] == "on") then uptable["holidayMode"] = 0x10 elseif (streams["holiday_mode"] == "off") then uptable["holidayMode"] = 0x00 end
    if (streams["moisturize_mode"] == "on") then uptable["moisturizeMode"] = 0x20 elseif (streams["moisturize_mode"] == "off") then uptable["moisturizeMode"] = 0x00 end
    if (streams["preservation_mode"] == "on") then uptable["preservationMode"] = 0x40 elseif (streams["preservation_mode"] == "off") then uptable["preservationMode"] = 0x00 end
    if (streams["acme_freezing_mode"] == "on") then uptable["acmeFreezingMode"] = 0x80 elseif (streams["acme_freezing_mode"] == "off") then uptable["acmeFreezingMode"] = 0x00 end
    if (streams["storage_temperature"] ~= nil and (streams["colmo_cool_freeze_mode"] == "2" or uptable["colmoCoolFreezeMode"] == 0x02)) then
        uptable["refrigerationTemperature"] = checkBoundary(streams["storage_temperature"], -20, 0)
        uptable["refrigerationTemperature"] = -11 - uptable["refrigerationTemperature"]
    elseif (streams["storage_temperature"] ~= nil) then uptable["refrigerationTemperature"] = checkBoundary(
        streams["storage_temperature"], -2, 20) end
    if (streams["freezing_temperature"] ~= nil and (streams["colmo_cool_freeze_mode"] == "1" or uptable["colmoCoolFreezeMode"] == 0x01)) then
        uptable["freezingTemperature"] = checkBoundary(streams["freezing_temperature"], -2, 10)
        uptable["freezingTemperature"] = uptable["freezingTemperature"] + 3
    elseif (streams["freezing_temperature"] ~= nil) then
        uptable["freezingTemperature"] = checkBoundary(streams["freezing_temperature"], -30, -10)
        uptable["freezingTemperature"] = uptable["freezingTemperature"] +
        (((-15 - uptable["freezingTemperature"]) * 2) + 18)
    end
    if (streams["left_flexzone_temperature"] ~= nil) then
        uptable["lVariableTemperature"] = checkBoundary(streams["left_flexzone_temperature"], -30, 20)
        if ((uptable["lVariableTemperature"] >= -18) and (uptable["lVariableTemperature"] <= 10)) then uptable["lVariableTemperature"] =
            uptable["lVariableTemperature"] + 19 elseif ((uptable["lVariableTemperature"] >= -24) and (uptable["lVariableTemperature"] <= -19)) then uptable["lVariableTemperature"] = 30 -
            uptable["lVariableTemperature"] else uptable["lVariableTemperature"] = 0 end
    end
    if (streams["right_flexzone_temperature"] ~= nil) then
        uptable["rVariableTemperature"] = checkBoundary(streams["right_flexzone_temperature"], -30, 20)
        if (uptable["rVariableTemperature"] == 0) then uptable["rVariableTemperature"] = 0 elseif ((uptable["rVariableTemperature"] >= -18) and (uptable["rVariableTemperature"] <= 10)) then uptable["rVariableTemperature"] =
            uptable["rVariableTemperature"] + 19 elseif ((uptable["rVariableTemperature"] >= -24) and (uptable["rVariableTemperature"] <= -19)) then uptable["rVariableTemperature"] = 30 -
            uptable["rVariableTemperature"] else uptable["rVariableTemperature"] = 0 end
    end
    if (streams["variable_mode"] == "soft_freezing_mode") then uptable["variableModeValue"] = 0x01 elseif (streams["variable_mode"] == "zero_fresh_mode") then uptable["variableModeValue"] = 0x02 elseif (streams["variable_mode"] == "cold_drink_mode") then uptable["variableModeValue"] = 0x03 elseif (streams["variable_mode"] == "fresh_product_mode") then uptable["variableModeValue"] = 0x04 elseif (streams["variable_mode"] == "partial_freezing_mode") then uptable["variableModeValue"] = 0x05 elseif (streams["variable_mode"] == "dry_zone_mode") then uptable["variableModeValue"] = 0x06 elseif (streams["variable_mode"] == "freeze_warm_mode") then uptable["variableModeValue"] = 0x07 elseif (streams["variable_mode"] == "freeze_mode") then uptable["variableModeValue"] = 0x08 end
    if (streams["storage_power"] == "on") then uptable["refrigerationPowerValue"] = 0x00 elseif (streams["storage_power"] == "off") then uptable["refrigerationPowerValue"] = 0x01 end
    if (streams["left_flexzone_power"] == "on") then uptable["lVariablePowerValue"] = 0x00 elseif (streams["left_flexzone_power"] == "off") then uptable["lVariablePowerValue"] = 0x04 end
    if (streams["right_flexzone_power"] == "on") then uptable["rVariablePowerValue"] = 0x00 elseif (streams["right_flexzone_power"] == "off") then uptable["rVariablePowerValue"] = 0x08 end
    if (streams["freezing_power"] == "on") then uptable["freezingPowerValue"] = 0x00 elseif (streams["freezing_power"] == "off") then uptable["freezingPowerValue"] = 0x10 end
    if (streams["cross_peak_electricity_enter"] == "enter") then uptable["crossPeakElectricityEnter"] = 0x20 elseif (streams["cross_peak_electricity_enter"] == "quit") then uptable["crossPeakElectricityEnter"] = 0x00 end
    if (streams["cross_peak_electricity"] == "on") then uptable["crossPeakElectricity"] = 0x40 elseif (streams["cross_peak_electricity"] == "off") then uptable["crossPeakElectricity"] = 0x00 end
    if (streams["all_refrigeration_power"] == "on") then uptable["allRefrigerationPower"] = 0x80 elseif (streams["all_refrigeration_power"] == "off") then uptable["allRefrigerationPower"] = 0x00 end
    if (streams["remove_dew_power"] == "on") then uptable["removeDew"] = 0x01 elseif (streams["remove_dew_power"] == "off") then uptable["removeDew"] = 0x00 end
    if (streams["humidify_power"] == "on") then uptable["humidify"] = 0x02 elseif (streams["humidify_power"] == "off") then uptable["humidify"] = 0x00 end
    if (streams["unfreeze_power"] == "on") then uptable["unfreeze"] = 0x04 elseif (streams["unfreeze_power"] == "off") then uptable["unfreeze"] = 0x00 end
    if (streams["temperature_unit"] == "fahrenheit") then uptable["temperatureUnit"] = 0x08 elseif (streams["temperature_unit"] == "celsius") then uptable["temperatureUnit"] = 0x00 end
    if (streams["floodlight_power"] == "on") then uptable["floodlight"] = 0x10 elseif (streams["floodlight_power"] == "off") then uptable["floodlight"] = 0x00 end
    if (streams["icea_bar_function_switch"] == "default") then uptable["functionSwitch"] = 0x00 elseif (streams["icea_bar_function_switch"] == "refrigeration") then uptable["functionSwitch"] = 0x40 elseif (streams["icea_bar_function_switch"] == "freezing") then uptable["functionSwitch"] = 0x80 end
    if (streams["radar_mode_power"] == "on") then uptable["radarMode"] = 0x01 elseif (streams["radar_mode_power"] == "off") then uptable["radarMode"] = 0x00 end
    if (streams["milk_mode_power"] == "on") then uptable["milkMode"] = 0x02 elseif (streams["milk_mode_power"] == "off") then uptable["milkMode"] = 0x00 end
    if (streams["icea_mode_power"] == "on") then uptable["icedMode"] = 0x04 elseif (streams["icea_mode_power"] == "off") then uptable["icedMode"] = 0x00 end
    if (streams["plasma_aseptic_mode_power"] == "on") then uptable["plasmaAsepticMode"] = 0x08 elseif (streams["plasma_aseptic_mode_power"] == "off") then uptable["plasmaAsepticMode"] = 0x00 end
    if (streams["acquire_icea_mode_power"] == "on") then uptable["acquireIceaMode"] = 0x10 elseif (streams["acquire_icea_mode_power"] == "off") then uptable["acquireIceaMode"] = 0x00 end
    if (streams["brash_icea_mode_power"] == "on") then uptable["brashIceaMode"] = 0x20 elseif (streams["brash_icea_mode_power"] == "off") then uptable["brashIceaMode"] = 0x00 end
    if (streams["acquire_water_mode_power"] == "on") then uptable["acquireWaterMode"] = 0x40 elseif (streams["acquire_water_mode_power"] == "off") then uptable["acquireWaterMode"] = 0x00 end
    if (streams["freezing_ice_machine_power"] == "on") then uptable["freezingIceMachinePower"] = 0x80 elseif (streams["freezing_ice_machine_power"] == "off") then uptable["freezingIceMachinePower"] = 0x00 end
    if (streams["human_induction_status"] == "valid") then uptable["humanInduction"] = 0x10 elseif (streams["human_induction_status"] == "invalid") then uptable["humanInduction"] = 0x00 end
    if (streams["human_induction_light_switch"] == "on") then uptable["humanInductionLightSwitch"] = 0x40 elseif (streams["human_induction_light_switch"] == "off") then uptable["humanInductionLightSwitch"] = 0x00 end
    if (streams["interval_room_humidity_level"] ~= nil) then uptable["intervalRoomHumidityLevel"] = checkBoundary(
        streams["interval_room_humidity_level"], 0, 127) end
    if (streams["food_site"] == "left_freezing_room") then uptable["foodSite"] = 0x00 elseif (streams["food_site"] == "right_freezing_room") then uptable["foodSite"] = 0x01 end
    if (streams["microcrystal_fresh"] == "on") then uptable["microcrystalFresh"] = 0x01 elseif (streams["microcrystal_fresh"] == "off") then uptable["microcrystalFresh"] = 0x00 end
    if (streams["dry_zone"] == "on") then uptable["dryZone"] = 0x02 elseif (streams["dry_zone"] == "off") then uptable["dryZone"] = 0x00 end
    if (streams["electronic_smell"] == "on") then uptable["electronicSmell"] = 0x04 elseif (streams["electronic_smell"] == "off") then uptable["electronicSmell"] = 0x00 end
    if (streams["eradicate_pesticide_residue"] == "on") then uptable["eradicatePesticideResidue"] = 0x08 elseif (streams["eradicate_pesticide_residue"] == "off") then uptable["eradicatePesticideResidue"] = 0x00 end
    if (streams["humidity"] == "high") then uptable["humidity"] = 0x10 elseif (streams["humidity"] == "low") then uptable["humidity"] = 0x20 end
    if (streams["performance_mode"] == "on") then uptable["performanceMode"] = 0x80 elseif (streams["performance_mode"] == "off") then uptable["performanceMode"] = 0x00 end
    if (streams["normal_zone_level"] ~= nil) then uptable["normalTemperatureLevel"] = checkBoundary(
        streams["normal_zone_level"], 1, 10) end
    if (streams["function_zone_level"] ~= nil) then uptable["functionZoneLevel"] = checkBoundary(
        streams["function_zone_level"], 1, 10) end
    if (streams["humidify_setting"] ~= nil) then uptable["humiditySetting"] = checkBoundary(streams["humidify_setting"],
            1, 99) end
    if (streams["smart_humidify"] == "on") then uptable["smartHumidity"] = 0x80 elseif (streams["smart_humidify"] == "off") then uptable["smartHumidity"] = 0x00 end
    if (streams["storage_left_door_auto"] == "on") then uptable["storageLeftDoorAuto"] = 0x01 elseif (streams["storage_left_door_auto"] == "off") then uptable["storageLeftDoorAuto"] = 0x02 elseif (streams["storage_left_door_auto"] == "invalid") then uptable["storageLeftDoorAuto"] = 0x00 end
    if (streams["storage_right_door_auto"] == "on") then uptable["storageRightDoorAuto"] = 0x04 elseif (streams["storage_right_door_auto"] == "off") then uptable["storageRightDoorAuto"] = 0x08 elseif (streams["storage_right_door_auto"] == "invalid") then uptable["storageRightDoorAuto"] = 0x00 end
    if (streams["freezer_door_auto"] == "on") then uptable["freezerDoorAuto"] = 0x10 elseif (streams["freezer_door_auto"] == "off") then uptable["freezerDoorAuto"] = 0x20 elseif (streams["freezer_door_auto"] == "invalid") then uptable["freezerDoorAuto"] = 0x00 end
    if (streams["freezer_door_auto_control"] == "on") then uptable["freezerDoorAutoControl"] = 0x40 elseif (streams["freezer_door_auto_control"] == "off") then uptable["freezerDoorAutoControl"] = 0x00 end
    if (streams["storage_door_auto_control"] == "on") then uptable["storageDoorAutoControl"] = 0x80 elseif (streams["storage_door_auto_control"] == "off") then uptable["storageDoorAutoControl"] = 0x00 end
    if (streams["flex_door_auto"] == "on") then uptable["flexDoorAuto"] = 0x10 elseif (streams["flex_door_auto"] == "off") then uptable["flexDoorAuto"] = 0x20 elseif (streams["flex_door_auto"] == "invalid") then uptable["flexDoorAuto"] = 0x00 end
    if (streams["freezer_down_door_auto"] == "on") then uptable["freezerDownDoorAuto"] = 0x40 elseif (streams["freezer_down_door_auto"] == "off") then uptable["freezerDownDoorAuto"] = 0x80 elseif (streams["freezer_down_door_auto"] == "invalid") then uptable["freezerDownDoorAuto"] = 0x00 end
    if (streams["storage_ice_machine_power"] == "on") then uptable["storageIceMachinePower"] = 0x01 elseif (streams["storage_ice_machine_power"] == "off") then uptable["storageIceMachinePower"] = 0x00 end
    if (streams["filter_replacement_warning_elimination"] == "valid") then uptable["filterReplacementWarningElimination"] = 0x80 elseif (streams["filter_replacement_warning_elimination"] == "invalid") then uptable["filterReplacementWarningElimination"] = 0x00 end
    if (streams["storage_F_temperature"] ~= nil) then uptable["storageFTemperature"] = checkBoundary(
        streams["storage_F_temperature"], 10, 50) end
    if (streams["freezing_F_temperature"] ~= nil) then
        uptable["freezingFTemperature"] = checkBoundary(streams["freezing_F_temperature"], -20, 20)
        uptable["freezingFTemperature"] = 11 - uptable["freezingFTemperature"]
    end
    if (streams["left_flexzone_F_temperature"] ~= nil) then uptable["leftFlexzoneFTemperature"] = checkBoundary(
        streams["left_flexzone_F_temperature"], 10, 50) + 1 end
    if (streams["electronic_clean_strong"] == "on") then uptable["electronicCleanStrong"] = 0x01 elseif (streams["electronic_clean_strong"] == "off") then uptable["electronicCleanStrong"] = 0x00 end
    if (streams["quick_beverage_time"] ~= nil) then uptable["quickBeverageTime"] = checkBoundary(
        streams["quick_beverage_time"], 0, 127) end
    if (streams["quick_beverage"] == "on") then uptable["quickBeverage"] = 0x80 elseif (streams["quick_beverage"] == "off") then uptable["quickBeverage"] = 0x00 end
    if (streams["aquatic_product"] == "on") then uptable["aquaticProduct"] = 0x01 elseif (streams["aquatic_product"] == "off") then uptable["aquaticProduct"] = 0x00 end
    if (streams["silent_night_mode"] == "on") then uptable["silentNightMode"] = 0x04 elseif (streams["silent_night_mode"] == "off") then uptable["silentNightMode"] = 0x00 end
    if (streams["silent_mode"] == "on") then uptable["silentMode"] = 0x08 elseif (streams["silent_mode"] == "off") then uptable["silentMode"] = 0x00 end
    if (streams["deep_cold_mode"] == "on") then uptable["deepColdMode"] = 0x08 elseif (streams["deep_cold_mode"] == "off") then uptable["deepColdMode"] = 0x00 end
    if (streams["vacuum_mode"] == "on") then uptable["vacuumMode"] = 0x10 elseif (streams["vacuum_mode"] == "off") then uptable["vacuumMode"] = 0x00 end
    if (streams["vacuum_completed"] == "yes") then uptable["vacuumCompleted"] = 0x20 elseif (streams["vacuum_completed"] == "no") then uptable["vacuumCompleted"] = 0x00 end
    if (streams["night_mode"] == "on") then uptable["nightMode"] = 0x20 elseif (streams["night_mode"] == "off") then uptable["nightMode"] = 0x00 end
    if (streams["storage_light_level"] ~= nil) then uptable["storageLightLevel"] = checkBoundary(
        streams["storage_light_level"], -5, 30) end
    if (streams["voice_door_auto"] == "on") then uptable["voiceDoorAuto"] = 0x01 elseif (streams["voice_door_auto"] == "off") then uptable["voiceDoorAuto"] = 0x00 end
    if (streams["touch_door_auto"] == "on") then uptable["touchDoorAuto"] = 0x02 elseif (streams["touch_door_auto"] == "off") then uptable["touchDoorAuto"] = 0x00 end
    if (streams["help_door_auto"] == "on") then uptable["helpDoorAuto"] = 0x04 elseif (streams["help_door_auto"] == "off") then uptable["helpDoorAuto"] = 0x00 end
    if (streams["speed_door_open"] == "fast") then uptable["speedDoorOpen"] = 0x08 elseif (streams["speed_door_open"] == "slow") then uptable["speedDoorOpen"] = 0x00 end
    if (streams["angle_door_open"] == "90") then uptable["angleDoorOpen"] = 0x10 elseif (streams["angle_door_open"] == "110") then uptable["angleDoorOpen"] = 0x20 elseif (streams["angle_door_open"] == "135") then uptable["angleDoorOpen"] = 0x30 end
    if (streams["voice_assistant"] == "on") then uptable["voiceAssistant"] = 0x40 elseif (streams["voice_assistant"] == "off") then uptable["voiceAssistant"] = 0x00 end
    if (streams["no_action_door_close"] == "on") then uptable["noActionDoorClose"] = 0x80 elseif (streams["no_action_door_close"] == "off") then uptable["noActionDoorClose"] = 0x00 end
    if (streams["food_expire_light"] == "on") then uptable["foodExpireLight"] = 0x08 elseif (streams["food_expire_light"] == "off") then uptable["foodExpireLight"] = 0x00 end
    if (streams["level_msg_light"] == "on") then uptable["levelMsgLight"] = 0x10 elseif (streams["level_msg_light"] == "off") then uptable["levelMsgLight"] = 0x00 end
    if (streams["level_msg_light"] == "on") then uptable["levelMsgLight"] = 0x10 elseif (streams["level_msg_light"] == "off") then uptable["levelMsgLight"] = 0x00 end
    if (streams["rapid_ice_making"] == "on") then uptable["quickIceMode"] = 0x20 elseif (streams["rapid_ice_making"] == "off") then uptable["quickIceMode"] = 0x00 end
    if (streams["no_action_door_close_time"] == "60") then uptable["noActionDoorCloseTime"] = 0x00 elseif (streams["no_action_door_close_time"] == "45") then uptable["noActionDoorCloseTime"] = 0x40 elseif (streams["no_action_door_close_time"] == "30") then uptable["noActionDoorCloseTime"] = 0x80 end
    if (streams["beverage_vial_number"] ~= nil) then uptable["beverageVialNumber"] = checkBoundary(
        streams["beverage_vial_number"], -5, 300) end
    if (streams["beverage_mid_number"] ~= nil) then uptable["beverageMidNumber"] = checkBoundary(
        streams["beverage_mid_number"], -5, 300) end
    if (streams["beverage_big_number"] ~= nil) then uptable["beverageBigNumber"] = checkBoundary(
        streams["beverage_big_number"], -5, 300) end
    if (streams["beverage_quick_time"] ~= nil) then uptable["beverageQuickTime"] = checkBoundary(
        streams["beverage_quick_time"], -5, 100) end
    if (streams["lighting_effect"] ~= nil) then uptable["lightingEffect"] = checkBoundary(streams["lighting_effect"], -5,
            100) end
    if (streams["lighting_color"] ~= nil) then uptable["lightingColor"] = checkBoundary(streams["lighting_color"], -5,
            100) end
    if (streams["custom_color_R"] ~= nil) then uptable["customColorR"] = checkBoundary(streams["custom_color_R"], -5, 300) end
    if (streams["custom_color_G"] ~= nil) then uptable["customColorG"] = checkBoundary(streams["custom_color_G"], -5, 300) end
    if (streams["custom_color_B"] ~= nil) then uptable["customColorB"] = checkBoundary(streams["custom_color_B"], -5, 300) end
    if (streams["turn_off_light"] == "on") then uptable["turnOffLight"] = 0x00 elseif (streams["turn_off_light"] == "off") then uptable["turnOffLight"] = 0x01 end
    if (streams["light_brightness"] == "low") then uptable["lightBrightness"] = 0x02 elseif (streams["light_brightness"] == "high") then uptable["lightBrightness"] = 0x00 end
    if (streams["sunny_for_seven_days"] == "on") then uptable["sunnyForSevenDays"] = 0x04 elseif (streams["sunny_for_seven_days"] == "off") then uptable["sunnyForSevenDays"] = 0x00 end
    if (streams["tesla_handle_switch_mode"] == "on") then uptable["teslaHandleSwitchMode"] = 0x01 elseif (streams["tesla_handle_switch_mode"] == "off") then uptable["teslaHandleSwitchMode"] = 0x00 end
    if (streams["five_preservation_mode"] == "on") then uptable["fivePreservationMode"] = 0x02 elseif (streams["five_preservation_mode"] == "off") then uptable["fivePreservationMode"] = 0x00 end
    if (streams["night_light_switch"] == "on") then uptable["nightLightSwitch"] = 0x10 elseif (streams["night_light_switch"] == "off") then uptable["nightLightSwitch"] = 0x00 end
    if (streams["open_door_tips_switch"] == "on") then uptable["openDoorTipsSwitch"] = 0x20 elseif (streams["open_door_tips_switch"] == "off") then uptable["openDoorTipsSwitch"] = 0x00 end
    if (streams["pulse_switch"] == "on") then uptable["pulseSwitch"] = 0x40 elseif (streams["pulse_switch"] == "off") then uptable["pulseSwitch"] = 0x00 end
    if (streams["delivery_mode"] == "on") then uptable["deliveryMode"] = 0x80 elseif (streams["delivery_mode"] == "off") then uptable["deliveryMode"] = 0x00 end
    if (streams["sabbath_exit_time"] ~= nil) then uptable["sabbathExitTime"] = checkBoundary(
        streams["sabbath_exit_time"], -1, 60) end
    if (streams["sabbath_mode"] == "on") then uptable["sabbathMode"] = 0x40 elseif (streams["sabbath_mode"] == "off") then uptable["sabbathMode"] = 0x80 elseif (streams["sabbath_mode"] == "hold") then uptable["sabbathMode"] = 0x00 end
    if (streams["control_sugar_flag"] == "on") then uptable["controlSugarFlag"] = 0x04 elseif (streams["control_sugar_flag"] == "off") then uptable["controlSugarFlag"] = 0x00 end
    if (streams["strong_control_sugar_flag"] == "on") then uptable["strongControlSugarFlag"] = 0x08 elseif (streams["strong_control_sugar_flag"] == "off") then uptable["strongControlSugarFlag"] = 0x00 end
    if (streams["handle_return_time"] ~= nil) then uptable["handleReturnTime"] = checkBoundary(
        streams["handle_return_time"], -5, 300) end
    if (streams["delay_defrost_switch"] == "on") then uptable["delayDefrostSwitch"] = 0x01 elseif (streams["delay_defrost_switch"] == "off") then uptable["delayDefrostSwitch"] = 0x00 end
    if (streams["demand_response_switch"] == "on") then uptable["demandResponseSwitch"] = 0x02 elseif (streams["demand_response_switch"] == "off") then uptable["demandResponseSwitch"] = 0x00 end
    if (streams["temporary_deloading_switch"] == "on") then uptable["temporaryDeloadingSwitch"] = 0x04 elseif (streams["temporary_deloading_switch"] == "off") then uptable["temporaryDeloadingSwitch"] = 0x00 end
    if (streams["deloading_maximum_exit_time"] ~= nil) then
        uptable["deloadingMaximumExitTime"] = checkBoundary(streams["deloading_maximum_exit_time"], 0, 30)
        uptable["deloadingMaximumExitTime"] = uptable["deloadingMaximumExitTime"] * 0.5
    end
    if (streams["internal_deloading_maximum_exit_time"] ~= nil) then
        uptable["internalDeloadingMaximumExitTime"] = checkBoundary(streams["internal_deloading_maximum_exit_time"], 0,
            30)
        uptable["internalDeloadingMaximumExitTime"] = uptable["internalDeloadingMaximumExitTime"] * 0.5
    end
    if (streams["defrost_maximum_exit_time"] ~= nil) then
        uptable["defrostMaximumExitTime"] = checkBoundary(streams["defrost_maximum_exit_time"], 0, 15)
        uptable["defrostMaximumExitTime"] = uptable["defrostMaximumExitTime"] * 2
    end
    if (streams["demand_response_maximum_exit_time"] ~= nil) then
        uptable["demandResponseMaximumExitTime"] = checkBoundary(streams["demand_response_maximum_exit_time"], 0, 15)
        uptable["demandResponseMaximumExitTime"] = uptable["demandResponseMaximumExitTime"] * 2
    end
    if (streams["off_peak_defrost_switch"] == "on") then uptable["offPeakDefrostSwitch"] = 0x08 elseif (streams["off_peak_defrost_switch"] == "off") then uptable["offPeakDefrostSwitch"] = 0x00 end
    if (streams["cool_threshold_upward_value"] ~= nil) then
        uptable["coolThresholdUpwardValue"] = checkBoundary(streams["cool_threshold_upward_value"], 0, 2)
        uptable["coolThresholdUpwardValue"] = uptable["coolThresholdUpwardValue"] * 2 - 1
    end
    if (streams["freeze_threshold_upward_value"] ~= nil) then
        uptable["freezeThresholdUpwardValue"] = checkBoundary(streams["freeze_threshold_upward_value"], 0, 2)
        uptable["freezeThresholdUpwardValue"] = uptable["freezeThresholdUpwardValue"] * 2 - 1
    end
    if (streams["ice_clean"] == "on") then uptable["iceClean"] = 0x08 elseif (streams["ice_clean"] == "off") then uptable["iceClean"] = 0x00 end
    if (streams["telstar_saving_mode"] == "on") then uptable["telstarSavingMode"] = 0x01 elseif (streams["telstar_saving_mode"] == "off") then uptable["telstarSavingMode"] = 0x00 end
    if (streams["panel_display_gear"] == "on") then uptable["panelDisplayGear"] = 0x02 elseif (streams["panel_display_gear"] == "off") then uptable["panelDisplayGear"] = 0x00 end
    if (streams["cooling_time_start_hour"] ~= nil) then uptable["coolingTimeStartHour"] = checkBoundary(
        streams["cooling_time_start_hour"], -5, 300) end
    if (streams["cooling_time_start_minutes"] ~= nil) then uptable["coolingTimeStartMinutes"] = checkBoundary(
        streams["cooling_time_start_minutes"], -5, 300) end
    if (streams["rise_time_start_hour"] ~= nil) then uptable["riseTimeStartHour"] = checkBoundary(
        streams["rise_time_start_hour"], -5, 300) end
    if (streams["rise_time_start_minutes"] ~= nil) then uptable["riseTimeStartMinutes"] = checkBoundary(
        streams["rise_time_start_minutes"], -5, 300) end
    if (streams["storage_left_door_auto_open_angle"] ~= nil) then uptable["storageLeftDoorAutoOpenAngle"] = checkBoundary(
        streams["storage_left_door_auto_open_angle"], -5, 30) end
    if (streams["storage_right_door_auto_open_angle"] ~= nil) then uptable["storageRightDoorAutoOpenAngle"] =
        checkBoundary(streams["storage_right_door_auto_open_angle"], -5, 30) end
    if (streams["global_flex_temperature"] ~= nil) then
        uptable["globalFlexTemperature"] = checkBoundary(streams["global_flex_temperature"], -35, 0)
        uptable["globalFlexTemperature"] = -uptable["globalFlexTemperature"] - 12
    end
    if (streams["quick_freezing"] == "on") then uptable["quickFreezing"] = 0x10 elseif (streams["quick_freezing"] == "off") then uptable["quickFreezing"] = 0x00 end
    if (streams["standby_mode"] == "on") then uptable["standbyMode"] = 0x08 elseif (streams["standby_mode"] == "off") then uptable["standbyMode"] = 0x00 end
    if (streams["freezing_light_open"] ~= nil) then uptable["freezingLightOpen"] = checkBoundary(
        streams["freezing_light_open"], 0, 100) end
    if (streams["storage_glass_door_light"] ~= nil) then uptable["storageGlassDoorLight"] = checkBoundary(
        streams["storage_glass_door_light"], 0, 100) end
    if (streams["storage_glass_door_light_open"] ~= nil) then uptable["storageGlassDoorLightOpen"] = checkBoundary(
        streams["storage_glass_door_light_open"], 0, 100) end
    if (streams["vegetable_freezing"] == "on") then uptable["vegetableFreezing"] = 0x40 elseif (streams["vegetable_freezing"] == "off") then uptable["vegetableFreezing"] = 0x00 end
    if (streams["vegetable_freezing_dry"] == "on") then uptable["vegetableFreezingDry"] = 0x80 elseif (streams["vegetable_freezing_dry"] == "off") then uptable["vegetableFreezingDry"] = 0x00 end
    if (streams["storage_door_auto_open"] == "full") then uptable["storageDoorAutoOpen"] = 0x01 elseif (streams["storage_door_auto_open"] == "single") then uptable["storageDoorAutoOpen"] = 0x00 end
    if (streams["freezing_light_open_chose"] == "on") then uptable["freezingLightOpenChose"] = 0x20 elseif (streams["freezing_light_open_chose"] == "off") then uptable["freezingLightOpenChose"] = 0x00 end
    if (streams["storage_light_open_chose"] == "on") then uptable["storageLightOpenChose"] = 0x08 elseif (streams["storage_light_open_chose"] == "off") then uptable["storageLightOpenChose"] = 0x00 end
    if (streams["smart_ai_to_self_select"] == "yes") then uptable["smartAiToSelfSelect"] = 0x08 elseif (streams["smart_ai_to_self_select"] == "no") then uptable["smartAiToSelfSelect"] = 0x00 end
    if (streams["ai_purine_2nd_estimate"] == "process") then uptable["aiPurine2ndEstimate"] = 0x10 elseif (streams["ai_purine_2nd_estimate"] == "finish") then uptable["aiPurine2ndEstimate"] = 0x00 end
    if (streams["surface_light_mode_select"] == "manual") then uptable["surfaceLightModeSelect"] = 0x20 elseif (streams["surface_light_mode_select"] == "automatic") then uptable["surfaceLightModeSelect"] = 0x00 end
    if (streams["atmosphere_lamp_mode_select"] == "manual") then uptable["atmosphereLampModeSelect"] = 0x40 elseif (streams["atmosphere_lamp_mode_select"] == "automatic") then uptable["atmosphereLampModeSelect"] = 0x00 end
    if (streams["tap_tap"] == "on") then uptable["tapTap"] = 0x02 elseif (streams["tap_tap"] == "off") then uptable["tapTap"] = 0x00 end
    if (streams["wine_type"] ~= nil) then uptable["wineType"] = checkBoundary(streams["wine_type"], -1, 100) end
    if (streams["ai_fruit_display_control"] ~= nil) then uptable["aiFruitDisplayControl"] = checkBoundary(
        streams["ai_fruit_display_control"], -1, 100) end
    if (streams["ai_fruit_flag"] == "on") then uptable["aiFruitFlag"] = 0x08 elseif (streams["ai_fruit_flag"] == "off") then uptable["aiFruitFlag"] = 0x00 end
    if (streams["ai_purine_display_control"] ~= nil) then uptable["aiPurineDisplayControl"] = checkBoundary(
        streams["ai_purine_display_control"], -1, 100) end
    if (streams["ai_purine_flag"] == "on") then uptable["aiPurineFlag"] = 0x80 elseif (streams["ai_purine_flag"] == "off") then uptable["aiPurineFlag"] = 0x00 end
    if (streams["ai_fruit_box_gear"] ~= nil) then uptable["aiFruitBoxGear"] = checkBoundary(streams["ai_fruit_box_gear"],
            -1, 100) end
    if (streams["offline_voice_switch"] == "on") then uptable["offlineVoiceSwitch"] = 0x10 elseif (streams["offline_voice_switch"] == "off") then uptable["offlineVoiceSwitch"] = 0x00 end
    if (streams["offline_voice_sensitivity"] ~= nil) then uptable["offlineVoiceSensitivity"] = checkBoundary(
        streams["offline_voice_sensitivity"], -1, 100) end
    if (streams["led_pwm_duty"] ~= nil) then uptable["ledPwmDuty"] = checkBoundary(streams["led_pwm_duty"], -1, 110) end
    if (streams["sleep_mode"] == "on") then uptable["sleepMode"] = 0x80 elseif (streams["sleep_mode"] == "off") then uptable["sleepMode"] = 0x00 end
    if (streams["sleep_mode_start_hour"] ~= nil) then uptable["sleepModeStartHour"] = checkBoundary(
        streams["sleep_mode_start_hour"], -1, 30) end
    if (streams["sleep_mode_start_minute"] ~= nil) then uptable["sleepModeStartMinute"] = checkBoundary(
        streams["sleep_mode_start_minute"], -1, 70) end
    if (streams["sleep_mode_end_hour"] ~= nil) then uptable["sleepModeEndHour"] = checkBoundary(
        streams["sleep_mode_end_hour"], -1, 30) end
    if (streams["sleep_mode_end_minute"] ~= nil) then uptable["sleepModeEndMinute"] = checkBoundary(
        streams["sleep_mode_end_minute"], -1, 70) end
    if (streams["ice_water_mode"] == "on") then uptable["iceWaterMode"] = 0x01 elseif (streams["ice_water_mode"] == "off") then uptable["iceWaterMode"] = 0x00 end
    if (streams["smart_recommend"] == "on") then uptable["smartRecommend"] = 0x02 elseif (streams["smart_recommend"] == "off") then uptable["smartRecommend"] = 0x00 end
    if (streams["divider_support_auto_fill"] == "yes") then uptable["dividerSupportAutoFill"] = 0x80 elseif (streams["divider_support_auto_fill"] == "no") then uptable["dividerSupportAutoFill"] = 0x00 end
    if (streams["ice_water_mix_type"] == "full") then uptable["iceWaterMixType"] = 0x00 elseif (streams["ice_water_mix_type"] == "smash") then uptable["iceWaterMixType"] = 0x08 end
    if (streams["ice_water_mix_proportion"] ~= nil) then uptable["iceWaterMixProportion"] = checkBoundary(
        streams["ice_water_mix_proportion"], -1, 10) end
    if (streams["ice_water_mix_type_morning"] == "full") then uptable["iceWaterMixTypeMorning"] = 0x00 elseif (streams["ice_water_mix_type_morning"] == "smash") then uptable["iceWaterMixTypeMorning"] = 0x10 end
    if (streams["ice_water_mix_proportion_morning"] ~= nil) then uptable["iceWaterMixProportionMorning"] = checkBoundary(
        streams["ice_water_mix_proportion_morning"], -1, 10) end
    if (streams["smart_noon_start_hour"] ~= nil) then uptable["smartNoonStartHour"] = checkBoundary(
        streams["smart_noon_start_hour"], -1, 30) end
    if (streams["ice_water_mix_type_noon"] == "full") then uptable["iceWaterMixTypeNoon"] = 0x00 elseif (streams["ice_water_mix_type_noon"] == "smash") then uptable["iceWaterMixTypeNoon"] = 0x10 end
    if (streams["ice_water_mix_proportion_noon"] ~= nil) then uptable["iceWaterMixProportionNoon"] = checkBoundary(
        streams["ice_water_mix_proportion_noon"], -1, 10) end
    if (streams["smart_night_start_hour"] ~= nil) then uptable["smartNightStartHour"] = checkBoundary(
        streams["smart_night_start_hour"], -1, 30) end
    if (streams["ice_water_mix_type_night"] == "full") then uptable["iceWaterMixTypeNight"] = 0x00 elseif (streams["ice_water_mix_type_night"] == "smash") then uptable["iceWaterMixTypeNight"] = 0x20 end
    uptable["iceWaterMixProportionNight"] = checkBoundary(streams["ice_water_mix_proportion_night"], -1, 10)
    if (streams["smart_morning_start_hour"] ~= nil) then uptable["smartMorningStartHour"] = checkBoundary(
        streams["smart_morning_start_hour"], -1, 30) end
    if (streams["open_door_warning_time"] ~= nil) then uptable["openDoorWarningTime"] = checkBoundary(
        streams["open_door_warning_time"], -1, 257) end
    if (streams["open_door_hover_time"] ~= nil) then uptable["openDoorHoverTime"] = checkBoundary(
        streams["open_door_hover_time"], -1, 257) end
    if (streams["camera_switch"] == "on") then uptable["cameraSwitch"] = 0x80 elseif (streams["camera_switch"] == "off") then uptable["cameraSwitch"] = 0x00 end
    if (streams["gps_report_switch"] == "on") then uptable["gpsReportSwitch"] = 0x01 elseif (streams["gps_report_switch"] == "off") then uptable["gpsReportSwitch"] = 0x00 end
    if (streams["room_led_dimming_flag"] == "on") then uptable["roomLedDimmingFlag"] = 0x20 elseif (streams["room_led_dimming_flag"] == "off") then uptable["roomLedDimmingFlag"] = 0x00 end
    if (streams["ice_machine_stop_ice_flag"] == "on") then uptable["iceMachineStopIceFlag"] = 0x40 elseif (streams["ice_machine_stop_ice_flag"] == "off") then uptable["iceMachineStopIceFlag"] = 0x00 end
    if (streams["display_board_mute_flag"] == "on") then uptable["displayBoardMuteFlag"] = 0x80 elseif (streams["display_board_mute_flag"] == "off") then uptable["displayBoardMuteFlag"] = 0x00 end
    if (streams["freezer_light_one_minute_flag"] == "on") then uptable["freezerLightOneMinuteFlag"] = 0x02 elseif (streams["freezer_light_one_minute_flag"] == "off") then uptable["freezerLightOneMinuteFlag"] = 0x00 end
    if (streams["is_have_freezing_ice"] == "yes") then uptable["isHaveFreezingIce"] = 0x40 elseif (streams["is_have_freezing_ice"] == "no") then uptable["isHaveFreezingIce"] = 0x00 end
    if (streams["handle_atmosphere_lamp_brightness"] ~= nil) then uptable["handleAtmosphereLampBrightness"] =
        checkBoundary(streams["handle_atmosphere_lamp_brightness"], -1, 10) end
    if (streams["colmo_cool_freeze_mode"] ~= nil) then uptable["colmoCoolFreezeMode"] = checkBoundary(
        streams["colmo_cool_freeze_mode"], -1, 4) end
    if (streams["tmf_cool_freeze_mode"] ~= nil) then uptable["tmfCoolFreezeMode"] = checkBoundary(
        streams["tmf_cool_freeze_mode"], -1, 10) end
    if (streams["app_smart_selection_mode"] == "on") then uptable["appSmartSelectionMode"] = 0x01 elseif (streams["app_smart_selection_mode"] == "off") then uptable["appSmartSelectionMode"] = 0x00 end
    if (streams["smart_selection_gear_change"] == "yes") then uptable["smartSelectionGearChange"] = 0x02 elseif (streams["smart_selection_gear_change"] == "no") then uptable["smartSelectionGearChange"] = 0x00 end
    if (streams["fridge_constant_temp_humidity"] == "on") then uptable["fridgeConstantTempHumidity"] = 0x04 elseif (streams["fridge_constant_temp_humidity"] == "off") then uptable["fridgeConstantTempHumidity"] = 0x00 end
    if (streams["smart_selection_set_temp"] ~= nil) then
        uptable["smartSelectionSetTemp"] = checkBoundary(streams["smart_selection_set_temp"], -10, 10)
        uptable["smartSelectionSetTemp"] = uptable["smartSelectionSetTemp"] + 50;
    end
    if (streams["electronic_clean_smart_mode"] == "on") then uptable["electronicCleanSmartMode"] = 0x40 elseif (streams["electronic_clean_smart_mode"] == "off") then uptable["electronicCleanSmartMode"] = 0x00 end
    if (streams["smart_freeze_mode"] == "on") then uptable["smartFreezeMode"] = 0x04 elseif (streams["smart_freeze_mode"] == "off") then uptable["smartFreezeMode"] = 0x00 end
    if (streams["smart_cool_mode"] == "on") then uptable["smartCoolMode"] = 0x08 elseif (streams["smart_cool_mode"] == "off") then uptable["smartCoolMode"] = 0x00 end
    if (streams["multi_func_zone_status"] == "off") then uptable["multiFuncZoneStatus"] = 0x10 elseif (streams["multi_func_zone_status"] == "on") then uptable["multiFuncZoneStatus"] = 0x00 end
    if (streams["defrost_mode_switch"] == "on") then uptable["defrostModeSwitch"] = 0x01 elseif (streams["defrost_mode_switch"] == "off") then uptable["defrostModeSwitch"] = 0x00 end
    if (streams["defrost_completed_state"] == "yes") then uptable["defrostCompletedState"] = 0x02 elseif (streams["defrost_completed_state"] == "no") then uptable["defrostCompletedState"] = 0x00 end
    if (streams["defrost_remain_time"] ~= nil) then
        uptable["defrostRemainTime"] = checkBoundary(streams["defrost_remain_time"], 0, 14400)
        uptable["defrostRemainTimeData110"] = uptable["defrostRemainTime"] % 64
        uptable["defrostRemainTimeData111"] = math.floor(uptable["defrostRemainTime"] / 64)
    end
    if (streams["defrost_time_user_defined"] ~= nil) then uptable["defrostTimeUserDefined"] = checkBoundary(
        streams["defrost_time_user_defined"], -1, 240) end
    if (streams["nfc_signal_board_enabled"] == "on") then uptable["nfcSignalBoardEnabled"] = 0x01 elseif (streams["nfc_signal_board_enabled"] == "off") then uptable["nfcSignalBoardEnabled"] = 0x01 else uptable["nfcSignalBoardEnabled"] = 0x01 end
    if (streams["hex_length"] ~= nil) then uptable["hexLength"] = checkBoundary(streams["hex_length"], -1, 200) end
    if (streams["food_clip_data116"] ~= nil) then uptable["foodClipData116"] = bit.bor(
        checkBoundary(streams["food_clip_data116"], -1, 1000), 0x00) end
    if (streams["food_clip_data117"] ~= nil) then uptable["foodClipData117"] = bit.bor(
        checkBoundary(streams["food_clip_data117"], -1, 1000), 0x00) end
    if (streams["wifi_human_induction_value"] ~= nil) then uptable["wifiHumanInductionValue"] = checkBoundary(
        streams["wifi_human_induction_value"], -1, 100) end
    if (streams["wifi_human_induction_far_value"] ~= nil) then uptable["wifiHumanInductionFarValue"] = checkBoundary(
        streams["wifi_human_induction_far_value"], -1, 100) end
    if (streams["wifi_human_induction_exist_value"] ~= nil) then uptable["wifiHumanInductionExistValue"] = checkBoundary(
        streams["wifi_human_induction_exist_value"], -1, 100) end
    if (streams["range_tracking_short_value"] ~= nil) then uptable["rangeTrackingShortValue"] = checkBoundary(
        streams["range_tracking_short_value"], -1, 100) end
    if (streams["range_tracking_far_value"] ~= nil) then uptable["rangeTrackingFarValue"] = checkBoundary(
        streams["range_tracking_far_value"], -1, 100) end
    if (streams["resist_spectrum_symmetry_disturb_ratio"] ~= nil) then uptable["resistSpectrumSymmetryDisturbRatio"] =
        checkBoundary(streams["resist_spectrum_symmetry_disturb_ratio"], -1, 100) end
    if (streams["resist_spectrum_symmetry_disturb_num"] ~= nil) then uptable["resistSpectrumSymmetryDisturbNum"] =
        checkBoundary(streams["resist_spectrum_symmetry_disturb_num"], -1, 100) end
    if (streams["ai_human_induction_similarity_value"] ~= nil) then uptable["aiHumanInductionSimilarityValue"] =
        checkBoundary(streams["ai_human_induction_similarity_value"], -1, 100) end
    if (streams["basic_power_saving_switch"] == "on") then uptable["basicPowerSavingSwitch"] = 0x01 elseif (streams["basic_power_saving_switch"] == "off") then uptable["basicPowerSavingSwitch"] = 0x00 end
    if (streams["smart_denoise_open_hours"] ~= nil) then uptable["smartDenoiseOpenHours"] = checkBoundary(
        streams["smart_denoise_open_hours"], 0, 24) end
    if (streams["smart_denoise_open_mins"] ~= nil) then uptable["smartDenoiseOpenMins"] = checkBoundary(
        streams["smart_denoise_open_mins"], 0, 60) end
    if (streams["freezer_elec_powerful_deodorize_switch"] == "on") then uptable["freezerElecPowerfulDeodorizeSwitch"] = 0x01 elseif (streams["freezer_elec_powerful_deodorize_switch"] == "off") then uptable["freezerElecPowerfulDeodorizeSwitch"] = 0x00 end
    if (streams["freezer_elec_powerful_deodorize_hour_time"] ~= nil) then uptable["freezerElecPowerfulDeodorizeHourTime"] =
        checkBoundary(streams["freezer_elec_powerful_deodorize_hour_time"], 0, 128) end
    if (streams["freezer_elec_powerful_deodorize_min_time"] ~= nil) then uptable["freezerElecPowerfulDeodorizeMinTime"] =
        checkBoundary(streams["freezer_elec_powerful_deodorize_min_time"], 0, 256) end
    if (streams["storage_elec_powerful_deodorize_hour_time"] ~= nil) then uptable["storageElecPowerfulDeodorizeHourTime"] =
        checkBoundary(streams["storage_elec_powerful_deodorize_hour_time"], 0, 256) end
end
local function binToModel(binData)
    if ((function(t)
            local c = 0; for _ in pairs(t) do c = c + 1 end
            return c
        end)(binData) < 6) then return nil end
    local messageBytes = binData
    if ((uptable["dataType"] == 0x02 and messageBytes[0] == 0x00) or (uptable["dataType"] == 0x03 and messageBytes[0] == 0x00) or (uptable["dataType"] == 0x04 and messageBytes[0] == 0x02)) then
        uptable["codeMode"] = bit.band(messageBytes[1], 0x01)
        uptable["freezingMode"] = bit.band(messageBytes[1], 0x02)
        uptable["smartMode"] = bit.band(messageBytes[1], 0x04)
        uptable["energySavingMode"] = bit.band(messageBytes[1], 0x08)
        uptable["holidayMode"] = bit.band(messageBytes[1], 0x10)
        uptable["moisturizeMode"] = bit.band(messageBytes[1], 0x20)
        uptable["preservationMode"] = bit.band(messageBytes[1], 0x40)
        uptable["acmeFreezingMode"] = bit.band(messageBytes[1], 0x80)
        uptable["refrigerationTemperature"] = bit.band(messageBytes[2], 0x0F)
        uptable["freezingTemperature"] = bit.rshift(bit.band(messageBytes[2], 0xF0), 4)
        uptable["lVariableTemperature"] = messageBytes[3]
        uptable["rVariableTemperature"] = messageBytes[4]
        uptable["variableModeValue"] = messageBytes[5]
        uptable["refrigerationPowerValue"] = bit.band(messageBytes[6], 0x01)
        uptable["lVariablePowerValue"] = bit.band(messageBytes[6], 0x04)
        uptable["rVariablePowerValue"] = bit.band(messageBytes[6], 0x08)
        uptable["freezingPowerValue"] = bit.band(messageBytes[6], 0x10)
        uptable["crossPeakElectricityEnter"] = bit.band(messageBytes[6], 0x20)
        uptable["crossPeakElectricity"] = bit.band(messageBytes[6], 0x40)
        uptable["allRefrigerationPower"] = bit.band(messageBytes[6], 0x80)
        uptable["removeDew"] = bit.band(messageBytes[7], 0x01)
        uptable["humidify"] = bit.band(messageBytes[7], 0x02)
        uptable["unfreeze"] = bit.band(messageBytes[7], 0x04)
        uptable["temperatureUnit"] = bit.band(messageBytes[7], 0x08)
        uptable["floodlight"] = bit.band(messageBytes[7], 0x10)
        uptable["functionSwitch"] = bit.band(messageBytes[7], 0xC0)
        uptable["radarMode"] = bit.band(messageBytes[8], 0x01)
        uptable["milkMode"] = bit.band(messageBytes[8], 0x02)
        uptable["icedMode"] = bit.band(messageBytes[8], 0x04)
        uptable["plasmaAsepticMode"] = bit.band(messageBytes[8], 0x08)
        uptable["acquireIceaMode"] = bit.band(messageBytes[8], 0x10)
        uptable["brashIceaMode"] = bit.band(messageBytes[8], 0x20)
        uptable["acquireWaterMode"] = bit.band(messageBytes[8], 0x40)
        uptable["freezingIceMachinePower"] = bit.band(messageBytes[8], 0x80)
        uptable["freezingFahrenheit"] = messageBytes[9]
        uptable["refrigerationFahrenheit"] = bit.band(messageBytes[10], 0xFC)
        uptable["leachExpireDay"] = messageBytes[11]
        if (#messageBytes > 13) then
            uptable["powerConsumptionLow"] = messageBytes[12]
            uptable["powerConsumptionHigh"] = messageBytes[13]
        end
        if (#messageBytes > 14) then
            uptable["freezingMotorResetStatus"] = bit.band(messageBytes[14], 0x01)
            uptable["freezingMotorDeicingStatus"] = bit.band(messageBytes[14], 0x02)
            uptable["freezingIceMachineWaterStatus"] = bit.band(messageBytes[14], 0x04)
            uptable["freezingAllIceStatus"] = bit.band(messageBytes[14], 0x08)
            uptable["humanInduction"] = bit.band(messageBytes[14], 0x10)
            uptable["freezerIcemakerWaterShortage"] = bit.band(messageBytes[14], 0x20)
            uptable["humanInductionLightSwitch"] = bit.band(messageBytes[14], 0x40)
        end
        if (#messageBytes > 15) then
            uptable["refrigerationDoorPower"] = bit.band(messageBytes[15], 0x01)
            uptable["freezingDoorPower"] = bit.band(messageBytes[15], 0x02)
            uptable["variableDoorPower"] = bit.band(messageBytes[15], 0x04)
            uptable["iceMouthPower"] = bit.band(messageBytes[15], 0x08)
            uptable["barDoorPower"] = bit.band(messageBytes[15], 0x10)
            uptable["storageIceHomeDoorState"] = bit.band(messageBytes[15], 0x20)
            uptable["isHaveFreezingIce"] = bit.band(messageBytes[15], 0x40)
        end
        if (#messageBytes > 16) then
            uptable["isError"] = bit.band(messageBytes[16], 0x01)
            uptable["intervalRoomHumidityLevel"] = bit.band(messageBytes[16], 0xFE)
        end
        uptable["refrigerationRealTemperature"] = messageBytes[17]
        uptable["freezingRealTemperature"] = messageBytes[18]
        uptable["lVariableRealTemperature"] = messageBytes[19]
        uptable["rVariableRealTemperature"] = messageBytes[20]
        if (#messageBytes > 22) then
            uptable["fastColdMinuteLow"] = messageBytes[21]
            uptable["fastColdMinuteHigh"] = messageBytes[22]
        end
        if (#messageBytes > 24) then
            uptable["fastFreezeMinuteLow"] = messageBytes[23]
            uptable["fastFreezeMinuteHigh"] = messageBytes[24]
        end
        if (#messageBytes > 25) then
            uptable["foodSite"] = bit.band(messageBytes[25], 0x0F)
            uptable["beef"] = bit.band(messageBytes[25], 0x40)
            uptable["pork"] = bit.band(messageBytes[25], 0x80)
            uptable["mutton"] = bit.band(messageBytes[26], 0x01)
            uptable["chicken"] = bit.band(messageBytes[26], 0x02)
            uptable["duckMeat"] = bit.band(messageBytes[26], 0x04)
            uptable["fish"] = bit.band(messageBytes[26], 0x08)
            uptable["shrimp"] = bit.band(messageBytes[26], 0x10)
            uptable["dumplings"] = bit.band(messageBytes[26], 0x20)
            uptable["gluePudding"] = bit.band(messageBytes[26], 0x40)
            uptable["iceCream"] = bit.band(messageBytes[26], 0x80)
            uptable["microcrystalFresh"] = bit.band(messageBytes[27], 0x01)
            uptable["dryZone"] = bit.band(messageBytes[27], 0x02)
            uptable["electronicSmell"] = bit.band(messageBytes[27], 0x04)
            uptable["eradicatePesticideResidue"] = bit.band(messageBytes[27], 0x08)
            uptable["humidity"] = bit.band(messageBytes[27], 0x70)
            uptable["performanceMode"] = bit.band(messageBytes[27], 0x80)
            uptable["normalTemperatureLevel"] = messageBytes[28]
            uptable["functionZoneLevel"] = messageBytes[29]
            if (#messageBytes > 30) then
                uptable["humiditySetting"] = bit.band(messageBytes[30], 0x7F)
                uptable["smartHumidity"] = bit.band(messageBytes[30], 0x80)
                if (#messageBytes > 31) then
                    uptable["storageLeftDoorAuto"] = bit.band(messageBytes[31], 0x03)
                    uptable["storageRightDoorAuto"] = bit.band(messageBytes[31], 0x0C)
                    uptable["freezerDoorAuto"] = bit.band(messageBytes[31], 0x30)
                    uptable["freezerDoorAutoControl"] = bit.band(messageBytes[31], 0x40)
                    uptable["storageDoorAutoControl"] = bit.band(messageBytes[31], 0x80)
                    uptable["eradicatePesticideResidueProgress"] = bit.band(messageBytes[32], 0x7F)
                    uptable["eradicatePesticideResidueCompletion"] = bit.band(messageBytes[32], 0x80)
                    if (#messageBytes > 33) then
                        uptable["storageIceMachinePower"] = bit.band(messageBytes[33], 0x01)
                        uptable["storageMotorResetStatus"] = bit.band(messageBytes[33], 0x02)
                        uptable["storageMotorResetStatus"] = bit.band(messageBytes[33], 0x04)
                        uptable["storageIceMachineWaterStatus"] = bit.band(messageBytes[33], 0x08)
                        uptable["storageAllIceStatus"] = bit.band(messageBytes[33], 0x10)
                        uptable["filterExpiresMildWarning"] = bit.band(messageBytes[33], 0x20)
                        uptable["filterExpiresSevereWarning"] = bit.band(messageBytes[33], 0x40)
                        uptable["iceRoomRealTemperature"] = messageBytes[34]
                        if (#messageBytes > 35) then
                            uptable["storageFTemperature"] = messageBytes[35]
                            uptable["freezingFTemperature"] = messageBytes[36]
                            uptable["leftFlexzoneFTemperature"] = messageBytes[37]
                            if (#messageBytes > 38) then
                                uptable["electronicCleanStrong"] = bit.band(messageBytes[38], 0x01)
                                uptable["electronicCleanTimeout"] = bit.band(messageBytes[38], 0xFE)
                                if (uptable["electronicCleanTimeout"] ~= 0) then uptable["electronicCleanTimeout"] = bit
                                    .rshift(uptable["electronicCleanTimeout"], 1) end
                                if (#messageBytes > 39) then
                                    uptable["quickBeverageTime"] = bit.band(messageBytes[39], 0x7F)
                                    uptable["quickBeverage"] = bit.band(messageBytes[39], 0x80)
                                    if (#messageBytes > 40) then
                                        uptable["aquaticProduct"] = bit.band(messageBytes[40], 0x01)
                                        uptable["blueRayMode"] = bit.band(messageBytes[40], 0x02)
                                        uptable["silentNightMode"] = bit.band(messageBytes[40], 0x04)
                                        uptable["deepColdMode"] = bit.band(messageBytes[40], 0x08)
                                        uptable["vacuumMode"] = bit.band(messageBytes[40], 0x10)
                                        uptable["vacuumCompleted"] = bit.band(messageBytes[40], 0x20)
                                        uptable["flexDoorAuto"] = bit.band(messageBytes[41], 0x30)
                                        uptable["silentMode"] = bit.band(messageBytes[41], 0x08)
                                        uptable["freezerDownDoorAuto"] = bit.band(messageBytes[41], 0xC0)
                                        if (#messageBytes > 42) then
                                            uptable["storageLightLevel"] = bit.band(messageBytes[42], 0x1F)
                                            uptable["nightMode"] = bit.band(messageBytes[42], 0x20)
                                            uptable["quickBeverageCompleted"] = bit.band(messageBytes[42], 0x40)
                                            uptable["voiceDoorAuto"] = bit.band(messageBytes[43], 0x01)
                                            uptable["touchDoorAuto"] = bit.band(messageBytes[43], 0x02)
                                            uptable["helpDoorAuto"] = bit.band(messageBytes[43], 0x04)
                                            uptable["speedDoorOpen"] = bit.band(messageBytes[43], 0x08)
                                            uptable["angleDoorOpen"] = bit.band(messageBytes[43], 0x30)
                                            uptable["voiceAssistant"] = bit.band(messageBytes[43], 0x40)
                                            uptable["noActionDoorClose"] = bit.band(messageBytes[43], 0x80)
                                            uptable["foodExpireLight"] = bit.band(messageBytes[44], 0x08)
                                            uptable["levelMsgLight"] = bit.band(messageBytes[44], 0x10)
                                            uptable["quickIceMode"] = bit.band(messageBytes[44], 0x20)
                                            uptable["noActionDoorCloseTime"] = bit.band(messageBytes[44], 0xC0)
                                            if (#messageBytes >= 45) then
                                                uptable["leachExpireDayHigh"] = messageBytes[45]
                                                uptable["filterNaturalTimeHigh"] = messageBytes[45]
                                                uptable["filterNaturalTimeLow"] = messageBytes[46]
                                                uptable["waterFlowPercentage"] = messageBytes[46]
                                                if (#messageBytes >= 47) then
                                                    uptable["beverageVialNumber"] = messageBytes[47]
                                                    uptable["beverageMidNumber"] = messageBytes[48]
                                                    uptable["beverageBigNumber"] = messageBytes[49]
                                                    uptable["beverageQuickTime"] = messageBytes[50]
                                                    if (#messageBytes >= 51) then
                                                        uptable["localTimeHour"] = messageBytes[51]
                                                        uptable["localTimeMinute"] = messageBytes[52]
                                                        uptable["localTimeSecond"] = messageBytes[53]
                                                        uptable["timeZone"] = messageBytes[54]
                                                        uptable["week"] = messageBytes[55]
                                                        uptable["day"] = messageBytes[56]
                                                        uptable["month"] = messageBytes[57]
                                                        uptable["year"] = messageBytes[58]
                                                        if (#messageBytes >= 59) then
                                                            uptable["eCleaningPercentage"] = messageBytes[59]
                                                            uptable["drinkValveEqualOpenHigh"] = messageBytes[60]
                                                            uptable["drinkValveEqualOpenLow"] = messageBytes[61]
                                                            uptable["inletValveEqualOpenHigh"] = messageBytes[62]
                                                            uptable["inletValveEqualOpenLow"] = messageBytes[63]
                                                            uptable["filterElementUsePercentage"] = messageBytes[64]
                                                            uptable["iceMakerTimesHigh"] = messageBytes[65]
                                                            uptable["iceMakerTimesLow"] = messageBytes[66]
                                                            if (#messageBytes >= 67) then
                                                                uptable["lightingEffect"] = bit.band(messageBytes[67],
                                                                    0x07)
                                                                uptable["lightingColor"] = bit.rshift(
                                                                bit.band(messageBytes[67], 0xF8), 3)
                                                                uptable["customColorR"] = messageBytes[68]
                                                                uptable["customColorG"] = messageBytes[69]
                                                                uptable["customColorB"] = messageBytes[70]
                                                                uptable["turnOffLight"] = bit.band(messageBytes[71], 0x01)
                                                                uptable["lightBrightness"] = bit.band(messageBytes[71],
                                                                    0x02)
                                                                uptable["sunnyForSevenDays"] = bit.band(messageBytes[71],
                                                                    0x04)
                                                                uptable["standbyMode"] = bit.band(messageBytes[71], 0x08)
                                                                uptable["quickFreezing"] = bit.band(messageBytes[71],
                                                                    0x10)
                                                                uptable["freezingLightOpenChose"] = bit.band(
                                                                messageBytes[71], 0x20)
                                                                uptable["freezingLightOpen"] = bit.rshift(
                                                                messageBytes[71], 6)
                                                                if (#messageBytes >= 72) then
                                                                    uptable["wifiHumanInductionValue"] = messageBytes
                                                                    [72]
                                                                    if (#messageBytes >= 73) then
                                                                        uptable["teslaHandleSwitchMode"] = bit.band(
                                                                        messageBytes[73], 0x01)
                                                                        uptable["fivePreservationMode"] = bit.band(
                                                                        messageBytes[73], 0x02)
                                                                        uptable["controlSugarFlag"] = bit.band(
                                                                        messageBytes[73], 0x04)
                                                                        uptable["strongControlSugarFlag"] = bit.band(
                                                                        messageBytes[73], 0x08)
                                                                        uptable["nightLightSwitch"] = bit.band(
                                                                        messageBytes[73], 0x10)
                                                                        uptable["openDoorTipsSwitch"] = bit.band(
                                                                        messageBytes[73], 0x20)
                                                                        uptable["pulseSwitch"] = bit.band(
                                                                        messageBytes[73], 0x40)
                                                                        uptable["deliveryMode"] = bit.band(
                                                                        messageBytes[73], 0x80)
                                                                        if (#messageBytes >= 74) then
                                                                            uptable["sabbathExitTime"] = bit.band(
                                                                            messageBytes[74], 0x3F)
                                                                            uptable["sabbathMode"] = bit.band(
                                                                            messageBytes[74], 0xC0)
                                                                            if (#messageBytes >= 75) then
                                                                                uptable["controlSugarTimeLow"] =
                                                                                messageBytes[75]
                                                                                uptable["controlSugarTimeHigh"] =
                                                                                messageBytes[76]
                                                                                if (#messageBytes >= 77) then
                                                                                    uptable["handleReturnTime"] =
                                                                                    messageBytes[77]
                                                                                    if (#messageBytes >= 78) then
                                                                                        uptable["delayDefrostSwitch"] =
                                                                                        bit.band(messageBytes[78], 0x01)
                                                                                        uptable["demandResponseSwitch"] =
                                                                                        bit.band(messageBytes[78], 0x02)
                                                                                        uptable["temporaryDeloadingSwitch"] =
                                                                                        bit.band(messageBytes[78], 0x04)
                                                                                        uptable["iceClean"] = bit.band(
                                                                                        messageBytes[78], 0x08)
                                                                                        uptable["deloadingMaximumExitTime"] =
                                                                                        bit.rshift(
                                                                                        bit.band(messageBytes[78], 0xF0),
                                                                                            4)
                                                                                    end
                                                                                    if (#messageBytes >= 79) then
                                                                                        uptable["defrostMaximumExitTime"] =
                                                                                        bit.band(messageBytes[79], 0x0F)
                                                                                        uptable["demandResponseMaximumExitTime"] =
                                                                                        bit.rshift(
                                                                                        bit.band(messageBytes[79], 0xF0),
                                                                                            4)
                                                                                    end
                                                                                    if (#messageBytes >= 80) then
                                                                                        uptable["telstarSavingMode"] =
                                                                                        bit.band(messageBytes[80], 0x01)
                                                                                        uptable["panelDisplayGear"] = bit
                                                                                        .band(messageBytes[80], 0x02)
                                                                                        uptable["offPeakDefrostSwitch"] =
                                                                                        bit.band(messageBytes[80], 0x08)
                                                                                        uptable["coolThresholdUpwardValue"] =
                                                                                        bit.rshift(
                                                                                        bit.band(messageBytes[80], 0x30),
                                                                                            4)
                                                                                        uptable["freezeThresholdUpwardValue"] =
                                                                                        bit.rshift(
                                                                                        bit.band(messageBytes[80], 0xC0),
                                                                                            6)
                                                                                        if (#messageBytes >= 84) then
                                                                                            uptable["coolingTimeStartHour"] =
                                                                                            messageBytes[81]
                                                                                            uptable["coolingTimeStartMinutes"] =
                                                                                            messageBytes[82]
                                                                                            uptable["riseTimeStartHour"] =
                                                                                            messageBytes[83]
                                                                                            uptable["riseTimeStartMinutes"] =
                                                                                            messageBytes[84]
                                                                                        end
                                                                                        if (#messageBytes >= 85) then
                                                                                            uptable["storageLeftDoorAutoOpenAngle"] =
                                                                                            bit.band(messageBytes[85],
                                                                                                0x0F)
                                                                                            uptable["storageRightDoorAutoOpenAngle"] =
                                                                                            bit.rshift(
                                                                                            bit.band(messageBytes[85],
                                                                                                0xF0), 4)
                                                                                            if (#messageBytes >= 86) then
                                                                                                uptable["globalFlexTemperature"] =
                                                                                                messageBytes[86]
                                                                                                if (#messageBytes >= 87) then
                                                                                                    uptable["storageGlassDoorLight"] =
                                                                                                    bit.band(
                                                                                                    messageBytes[87],
                                                                                                        0x07)
                                                                                                    uptable["storageLightOpenChose"] =
                                                                                                    bit.band(
                                                                                                    messageBytes[87],
                                                                                                        0x08)
                                                                                                    uptable["storageGlassDoorLightOpen"] =
                                                                                                    bit.rshift(
                                                                                                    bit.band(
                                                                                                    messageBytes[87],
                                                                                                        0x3F), 4)
                                                                                                    uptable["vegetableFreezing"] =
                                                                                                    bit.band(
                                                                                                    messageBytes[87],
                                                                                                        0x40)
                                                                                                    uptable["vegetableFreezingDry"] =
                                                                                                    bit.band(
                                                                                                    messageBytes[87],
                                                                                                        0x80)
                                                                                                    if (#messageBytes >= 88) then
                                                                                                        uptable["aiFruitDisplayControl"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[88],
                                                                                                            0x07)
                                                                                                        uptable["aiFruitFlag"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[88],
                                                                                                            0x08)
                                                                                                        uptable["aiPurineDisplayControl"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[88],
                                                                                                            0x70)
                                                                                                        uptable["aiPurineFlag"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[88],
                                                                                                            0x80)
                                                                                                        uptable["aiFruitBoxGear"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[89],
                                                                                                            0x07)
                                                                                                    end
                                                                                                    if (#messageBytes >= 89) then
                                                                                                        uptable["smartAiToSelfSelect"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[89],
                                                                                                            0x08)
                                                                                                        uptable["aiPurine2ndEstimate"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[89],
                                                                                                            0x10)
                                                                                                        uptable["surfaceLightModeSelect"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[89],
                                                                                                            0x20)
                                                                                                        uptable["atmosphereLampModeSelect"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[89],
                                                                                                            0x40)
                                                                                                    end
                                                                                                    if (#messageBytes >= 90) then
                                                                                                        uptable["storageDoorAutoOpen"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[90],
                                                                                                            0x01)
                                                                                                        uptable["tapTap"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[90],
                                                                                                            0x02)
                                                                                                        uptable["wineType"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[90],
                                                                                                            0x0C), 2)
                                                                                                        uptable["offlineVoiceSwitch"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[90],
                                                                                                            0x10)
                                                                                                        uptable["offlineVoiceSensitivity"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[90],
                                                                                                            0x60), 5)
                                                                                                        uptable["cameraSwitch"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[90],
                                                                                                            0x80)
                                                                                                    end
                                                                                                    if (#messageBytes >= 91) then
                                                                                                        uptable["ledPwmDuty"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[91],
                                                                                                            0x7F)
                                                                                                        uptable["sleepMode"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[91],
                                                                                                            0x80)
                                                                                                    end
                                                                                                    if (#messageBytes >= 92) then
                                                                                                        uptable["sleepModeStartHour"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[92],
                                                                                                            0x1F)
                                                                                                        uptable["roomLedDimmingFlag"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[92],
                                                                                                            0x20)
                                                                                                        uptable["iceMachineStopIceFlag"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[92],
                                                                                                            0x40)
                                                                                                        uptable["displayBoardMuteFlag"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[92],
                                                                                                            0x80)
                                                                                                        uptable["sleepModeStartMinute"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[93],
                                                                                                            0x3F)
                                                                                                        uptable["electronicCleanSmartMode"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[93],
                                                                                                            0x40)
                                                                                                        uptable["sleepModeEndHour"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[94],
                                                                                                            0x1F)
                                                                                                        uptable["sleepModeEndMinute"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[95],
                                                                                                            0x3F)
                                                                                                    end
                                                                                                    if (#messageBytes >= 96) then
                                                                                                        uptable["iceWaterMode"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[96],
                                                                                                            0x01)
                                                                                                        uptable["smartRecommend"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[96],
                                                                                                            0x02)
                                                                                                        uptable["autoFill"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[96],
                                                                                                            0x04)
                                                                                                        uptable["iceWaterMixType"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[96],
                                                                                                            0x08)
                                                                                                        uptable["iceWaterMixProportion"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[96],
                                                                                                            0x30), 4)
                                                                                                        uptable["overflowSensor"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[96],
                                                                                                            0x40)
                                                                                                        uptable["dividerSupportAutoFill"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[96],
                                                                                                            0x80)
                                                                                                        uptable["smartMorningStartHour"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[97],
                                                                                                            0x0F)
                                                                                                        uptable["iceWaterMixTypeMorning"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[97],
                                                                                                            0x10)
                                                                                                        uptable["iceWaterMixProportionMorning"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[97],
                                                                                                            0x60), 5)
                                                                                                        uptable["isMorningMode"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[97],
                                                                                                            0x80)
                                                                                                        uptable["smartNoonStartHour"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[98],
                                                                                                            0x0F)
                                                                                                        uptable["iceWaterMixTypeNoon"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[98],
                                                                                                            0x10)
                                                                                                        uptable["iceWaterMixProportionNoon"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[98],
                                                                                                            0x60), 5)
                                                                                                        uptable["isNoonMode"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[98],
                                                                                                            0x80)
                                                                                                        uptable["smartNightStartHour"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[99],
                                                                                                            0x0F)
                                                                                                        uptable["iceWaterMixTypeNight"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[99],
                                                                                                            0x10)
                                                                                                        uptable["iceWaterMixProportionNight"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[99],
                                                                                                            0x60), 5)
                                                                                                        uptable["isNightMode"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[99],
                                                                                                            0x80)
                                                                                                        uptable["waterBoxStatus"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[96],
                                                                                                            0x20), 5)
                                                                                                    end
                                                                                                    if (#messageBytes >= 100) then uptable["openDoorWarningTime"] =
                                                                                                        messageBytes[100] end
                                                                                                    if (#messageBytes >= 101) then uptable["openDoorHoverTime"] =
                                                                                                        messageBytes[101] end
                                                                                                    if (#messageBytes >= 102) then
                                                                                                        uptable["gpsReportSwitch"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[102],
                                                                                                            0x01)
                                                                                                        uptable["freezerLightOneMinuteFlag"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[102],
                                                                                                            0x02)
                                                                                                        uptable["smartFreezeMode"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[102],
                                                                                                            0x04)
                                                                                                        uptable["smartCoolMode"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[102],
                                                                                                            0x08)
                                                                                                        uptable["multiFuncZoneStatus"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[102],
                                                                                                            0x10)
                                                                                                    end
                                                                                                    if (#messageBytes >= 103) then
                                                                                                        uptable["appSmartSelectionMode"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[103],
                                                                                                            0x01)
                                                                                                        uptable["smartSelectionGearChange"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[103],
                                                                                                            0x02)
                                                                                                        uptable["fridgeConstantTempHumidity"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[103],
                                                                                                            0x04)
                                                                                                    end
                                                                                                    if (#messageBytes >= 104) then uptable["smartSelectionSetTemp"] =
                                                                                                        messageBytes[104] end
                                                                                                    if (#messageBytes >= 105) then uptable["tmfCoolFreezeMode"] =
                                                                                                        messageBytes[105] end
                                                                                                    if (#messageBytes >= 106) then
                                                                                                        uptable["handleAtmosphereLampBrightness"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[106],
                                                                                                            0x0F)
                                                                                                        uptable["colmoCoolFreezeMode"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[106],
                                                                                                            0x30), 4)
                                                                                                    end
                                                                                                    if (#messageBytes >= 110) then
                                                                                                        uptable["defrostModeSwitch"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[110],
                                                                                                            0x01)
                                                                                                        uptable["defrostCompletedState"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[110],
                                                                                                            0x02)
                                                                                                        uptable["defrostRemainTimeData110"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[110],
                                                                                                            0xFC), 2)
                                                                                                    end
                                                                                                    if (#messageBytes >= 111) then uptable["defrostRemainTimeData111"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[111],
                                                                                                            0xFF) end
                                                                                                    if (#messageBytes >= 112) then uptable["defrostTimeUserDefined"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[112],
                                                                                                            0xFF) end
                                                                                                    if (#messageBytes >= 113) then
                                                                                                        uptable["nfcSignalBoardEnabled"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[113],
                                                                                                            0x01)
                                                                                                        uptable["nfcSignalBoardState"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[113],
                                                                                                            0x08)
                                                                                                    end
                                                                                                    if (#messageBytes >= 117) then
                                                                                                        uptable["foodClipData116"] =
                                                                                                        bit.bor(
                                                                                                        messageBytes[116],
                                                                                                            0x00)
                                                                                                        uptable["foodClipData117"] =
                                                                                                        bit.bor(
                                                                                                        messageBytes[117],
                                                                                                            0x00)
                                                                                                    end
                                                                                                    if (#messageBytes >= 118) then uptable["wifiHumanInductionFarValue"] =
                                                                                                        messageBytes[118] end
                                                                                                    if (#messageBytes >= 119) then uptable["wifiHumanInductionExistValue"] =
                                                                                                        messageBytes[119] end
                                                                                                    if (#messageBytes >= 120) then uptable["rangeTrackingShortValue"] =
                                                                                                        messageBytes[120] end
                                                                                                    if (#messageBytes >= 121) then uptable["rangeTrackingFarValue"] =
                                                                                                        messageBytes[121] end
                                                                                                    if (#messageBytes >= 122) then uptable["resistSpectrumSymmetryDisturbRatio"] =
                                                                                                        messageBytes[122] end
                                                                                                    if (#messageBytes >= 123) then uptable["resistSpectrumSymmetryDisturbNum"] =
                                                                                                        messageBytes[123] end
                                                                                                    if (#messageBytes >= 124) then uptable["aiHumanInductionSimilarityValue"] =
                                                                                                        messageBytes[124] end
                                                                                                    if (#messageBytes >= 131) then
                                                                                                        uptable["basicPowerSavingSwitch"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[131],
                                                                                                            0x01)
                                                                                                        uptable["powerSavingStarVersion"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[131],
                                                                                                            0x02)
                                                                                                    end
                                                                                                    if (#messageBytes >= 132) then uptable["internalDeloadingMaximumExitTime"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[132],
                                                                                                            0xFF) end
                                                                                                    if (#messageBytes >= 133) then uptable["smartDenoiseOpenHours"] =
                                                                                                        messageBytes[133] end
                                                                                                    if (#messageBytes >= 134) then uptable["smartDenoiseOpenMins"] =
                                                                                                        messageBytes[134] end
                                                                                                    if (#messageBytes >= 135) then
                                                                                                        uptable["freezerElecPowerfulDeodorizeSwitch"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[135],
                                                                                                            0x01)
                                                                                                        uptable["freezerElecPowerfulDeodorizeHourTime"] =
                                                                                                        bit.rshift(
                                                                                                        bit.band(
                                                                                                        messageBytes[135],
                                                                                                            0xFE), 1)
                                                                                                    end
                                                                                                    if (#messageBytes >= 136) then uptable["freezerElecPowerfulDeodorizeMinTime"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[136],
                                                                                                            0xFF) end
                                                                                                    if (#messageBytes >= 137) then uptable["storageElecPowerfulDeodorizeHourTime"] =
                                                                                                        bit.band(
                                                                                                        messageBytes[137],
                                                                                                            0xFF) end
                                                                                                end
                                                                                            end
                                                                                        end
                                                                                    end
                                                                                end
                                                                            end
                                                                        end
                                                                    end
                                                                end
                                                            end
                                                        end
                                                    end
                                                end
                                            end
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end
    elseif ((uptable["dataType"] == 0x04 and messageBytes[0] == 0x01) or (uptable["dataType"] == 0x03 and messageBytes[0] == 0x01)) then
        uptable["codeMode"] = bit.band(messageBytes[33], 0x01)
        uptable["freezingMode"] = bit.band(messageBytes[33], 0x02)
        uptable["smartMode"] = bit.band(messageBytes[33], 0x04)
        uptable["energySavingMode"] = bit.band(messageBytes[33], 0x08)
        uptable["holidayMode"] = bit.band(messageBytes[33], 0x10)
        uptable["moisturizeMode"] = bit.band(messageBytes[33], 0x20)
        uptable["preservationMode"] = bit.band(messageBytes[33], 0x40)
        uptable["radarMode"] = bit.band(messageBytes[34], 0x01)
        uptable["milkMode"] = bit.band(messageBytes[34], 0x02)
        uptable["icedMode"] = bit.band(messageBytes[34], 0x04)
        uptable["plasmaAsepticMode"] = bit.band(messageBytes[34], 0x08)
        uptable["freezingIceMachinePower"] = bit.band(messageBytes[34], 0x10)
        uptable["acmeFreezingMode"] = bit.band(messageBytes[34], 0x20)
        uptable["removeDew"] = bit.band(messageBytes[35], 0x01)
        uptable["humidify"] = bit.band(messageBytes[35], 0x02)
        uptable["unfreeze"] = bit.band(messageBytes[35], 0x04)
        uptable["temperatureUnit"] = bit.band(messageBytes[35], 0x08)
        uptable["floodlight"] = bit.band(messageBytes[35], 0x10)
        uptable["functionSwitch"] = bit.band(messageBytes[35], 0xC0)
        uptable["refrigerationPowerValue"] = bit.band(messageBytes[36], 0x01)
        uptable["lVariablePowerValue"] = bit.band(messageBytes[36], 0x04)
        uptable["rVariablePowerValue"] = bit.band(messageBytes[36], 0x08)
        uptable["freezingPowerValue"] = bit.band(messageBytes[36], 0x10)
        uptable["allRefrigerationPower"] = bit.band(messageBytes[36], 0x80)
        uptable["refrigerationTemperature"] = messageBytes[37]
        uptable["freezingTemperature"] = messageBytes[38]
        uptable["lVariableTemperature"] = messageBytes[39]
        uptable["rVariableTemperature"] = messageBytes[40]
        uptable["intervalRoomHumidityLevel"] = messageBytes[42]
        uptable["refrigerationFahrenheit"] = messageBytes[43]
        uptable["freezingFahrenheit"] = messageBytes[44]
        uptable["variableModeValue"] = messageBytes[49]
        uptable["normalTemperatureLevel"] = messageBytes[50]
        uptable["functionZoneLevel"] = messageBytes[51]
        if (#messageBytes > 54) then
            uptable["microcrystalFresh"] = bit.band(messageBytes[56], 0x01)
            uptable["humidity"] = bit.band(messageBytes[56], 0x70)
            uptable["performanceMode"] = bit.band(messageBytes[56], 0x80)
            if (#messageBytes > 57) then
                uptable["electronicCleanStrong"] = bit.band(messageBytes[66], 0x01)
                uptable["electronicCleanTimeout"] = bit.band(messageBytes[66], 0xFE)
                if (uptable["electronicCleanTimeout"] ~= 0) then uptable["electronicCleanTimeout"] = bit.rshift(
                    uptable["electronicCleanTimeout"], 1) end
                if (#messageBytes > 83 and messageBytes[84] >= 0) then uptable["globalFlexTemperature"] = messageBytes
                    [84] end
            end
        end
    elseif (uptable["dataType"] == 0x04 and messageBytes[0] == 0x00) then
        uptable["refrigerationDoorPower"] = bit.band(messageBytes[1], 0x01)
        uptable["freezingDoorPower"] = bit.band(messageBytes[1], 0x02)
        uptable["barDoorPower"] = bit.band(messageBytes[1], 0x04)
        uptable["iceMouthPower"] = bit.band(messageBytes[1], 0x08)
        uptable["variableDoorPower"] = bit.band(messageBytes[1], 0x10)
        uptable["purineInhibitDrawerSwitch"] = bit.band(messageBytes[1], 0x20)
        if (#messageBytes > 2) then
            uptable["storageIceHomeDoorState"] = bit.band(messageBytes[2], 0x10)
            if (#messageBytes > 3) then
                uptable["storageModeCompletion"] = bit.band(messageBytes[3], 0x01)
                uptable["freezingModeCompletion"] = bit.band(messageBytes[3], 0x02)
                uptable["humidifierWaterShortage"] = bit.band(messageBytes[3], 0x04)
                uptable["plasmaAsepticCompletion"] = bit.band(messageBytes[3], 0x08)
                uptable["acmeFreezingCompletion"] = bit.band(messageBytes[3], 0x10)
                uptable["eradicatePesticideResidueCompletion"] = bit.band(messageBytes[3], 0x20)
                uptable["quickBeverageCompletion"] = bit.band(messageBytes[3], 0x80)
            end
        end
    elseif (uptable["dataType"] == 0x04 and messageBytes[0] == 0x04) then elseif ((uptable["dataType"] == 0x06 and messageBytes[0] == 0x01) or (uptable["dataType"] == 0x03 and messageBytes[0] == 0x02)) then
        if (messageBytes[1] ~= 0x00 or messageBytes[2] ~= 0x00 or messageBytes[3] ~= 0x00 or messageBytes[4] ~= 0x00 or messageBytes[5] ~= 0x00 or messageBytes[6] ~= 0x00 or messageBytes[7] ~= 0x00) then uptable["isError"] = 0x01 else uptable["isError"] = 0x00 end
        uptable["storageDoorOpenOvertime"] = bit.band(messageBytes[1], 0x01)
        uptable["freezerDoorOpenOvertime"] = bit.band(messageBytes[1], 0x02)
        uptable["barDoorOpenOvertime"] = bit.band(messageBytes[1], 0x04)
        uptable["variableDoorOpenOvertime"] = bit.band(messageBytes[1], 0x08)
        uptable["iceMachineFull"] = bit.band(messageBytes[1], 0x10)
        if (#messageBytes > 2) then
            uptable["refrigerationSensorError"] = bit.band(messageBytes[2], 0x01)
            uptable["refrigerationDefrostingSensorError"] = bit.band(messageBytes[2], 0x02)
            uptable["ringTemperatureSensorError"] = bit.band(messageBytes[2], 0x04)
            uptable["flexzoneSensorError"] = bit.band(messageBytes[2], 0x08)
            uptable["rightFlexzoneSensorError"] = bit.band(messageBytes[2], 0x10)
            uptable["freezingHighTemperature"] = bit.band(messageBytes[2], 0x20)
            uptable["freezingSensorError"] = bit.band(messageBytes[2], 0x40)
            uptable["freezingDefrostingSensorError"] = bit.band(messageBytes[2], 0x80)
            if (#messageBytes > 3) then
                uptable["iceElectricalMachineryError"] = bit.band(messageBytes[3], 0x01)
                uptable["refrigerationDefrostingOvertime"] = bit.band(messageBytes[3], 0x02)
                uptable["freezingDefrostingOvertime"] = bit.band(messageBytes[3], 0x04)
                uptable["zeroCrossingCheckError"] = bit.band(messageBytes[3], 0x08)
                uptable["eepromReadWriteError"] = bit.band(messageBytes[3], 0x10)
                uptable["leftFlexzoneSensorError"] = bit.band(messageBytes[3], 0x20)
                uptable["iceRoomSensorError"] = bit.band(messageBytes[3], 0x40)
                uptable["mainDisplayCorrespondError"] = bit.band(messageBytes[3], 0x80)
                if (#messageBytes > 4) then
                    uptable["iceMachineTemperatureError"] = bit.band(messageBytes[4], 0x01)
                    uptable["flexzoneDefrostingSensorError"] = bit.band(messageBytes[4], 0x02)
                    uptable["flexzoneDefrostingSensor2Error"] = bit.band(messageBytes[4], 0x04)
                    uptable["yogurtMachineSensorError"] = bit.band(messageBytes[4], 0x08)
                    uptable["iceMachineFrettingSwitchError"] = bit.band(messageBytes[4], 0x10)
                    uptable["iceMachinePipeFilterOvertime"] = bit.band(messageBytes[4], 0x20)
                    uptable["ambientHumiditySensorError"] = bit.band(messageBytes[4], 0x40)
                    uptable["storageHumiditySensorError"] = bit.band(messageBytes[4], 0x80)
                    if (#messageBytes > 5) then
                        uptable["radarSensor1Error"] = bit.band(messageBytes[5], 0x01)
                        uptable["radarSensor2Error"] = bit.band(messageBytes[5], 0x02)
                        uptable["radarSensor3Error"] = bit.band(messageBytes[5], 0x04)
                        uptable["radarSensor4Error"] = bit.band(messageBytes[5], 0x08)
                        uptable["radarSensor5Error"] = bit.band(messageBytes[5], 0x10)
                        uptable["functionZoneTemperatureSensorError"] = bit.band(messageBytes[5], 0x20)
                        uptable["normalZoneTemperatureSensorError"] = bit.band(messageBytes[5], 0x40)
                        uptable["humidityControlSensorError"] = bit.band(messageBytes[5], 0x80)
                        if (#messageBytes > 6) then
                            uptable["openDoorTooFrequently"] = bit.band(messageBytes[6], 0x01)
                            uptable["storageDoorAloneOpenFrequently"] = bit.band(messageBytes[6], 0x02)
                            uptable["freezingDoorAloneOpenFrequently"] = bit.band(messageBytes[6], 0x04)
                            uptable["barDoorAloneOpenFrequently"] = bit.band(messageBytes[6], 0x08)
                            uptable["snWritingError"] = bit.band(messageBytes[6], 0x20)
                            uptable["storageTemperatureOverheating"] = bit.band(messageBytes[6], 0x40)
                            uptable["storageTemperatureTooLow"] = bit.band(messageBytes[6], 0x80)
                            if (#messageBytes > 7) then
                                uptable["storageHeatingWireSensorError"] = bit.band(messageBytes[7], 0x01)
                                uptable["uartReceiverError"] = bit.band(messageBytes[7], 0x02)
                                uptable["crystalliteMainSensorError"] = bit.band(messageBytes[7], 0x08)
                                uptable["crystalliteBase1SensorError"] = bit.band(messageBytes[7], 0x10)
                                uptable["crystalliteBase2SensorError"] = bit.band(messageBytes[7], 0x20)
                                uptable["crystalliteBase3SensorError"] = bit.band(messageBytes[7], 0x40)
                                uptable["crystalliteBase4SensorError"] = bit.band(messageBytes[7], 0x80)
                                if (#messageBytes > 8) then
                                    uptable["iceRoomDoorOpenOvertime"] = bit.band(messageBytes[8], 0x01)
                                    uptable["storageIceFullTips"] = bit.band(messageBytes[8], 0x02)
                                    uptable["iceMachineSensorError"] = bit.band(messageBytes[8], 0x04)
                                    uptable["storageIceMachineSensorError"] = bit.band(messageBytes[8], 0x08)
                                    uptable["storageIceOperationError"] = bit.band(messageBytes[8], 0x10)
                                    uptable["freezingIceOperationError"] = bit.band(messageBytes[8], 0x20)
                                    uptable["mcuIceCommunicationError"] = bit.band(messageBytes[8], 0x40)
                                    if (#messageBytes > 10) then
                                        uptable["mcuFiveCommunicationError"] = bit.band(messageBytes[10], 0x01)
                                        uptable["fiveTslCommunicationError"] = bit.band(messageBytes[10], 0x02)
                                        uptable["twoTslCommunicationError"] = bit.band(messageBytes[10], 0x04)
                                        uptable["fiveNOError"] = bit.band(messageBytes[10], 0x08)
                                        uptable["fiveCTError"] = bit.band(messageBytes[10], 0x10)
                                        if (#messageBytes > 14) then uptable["freezerWaterShortageAlarm"] = bit.band(
                                            messageBytes[14], 0x20) end
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end
    end
end
function jsonToData(jsonCmd)
    if (#jsonCmd == 0) then return nil end
    local infoM = {}
    local bodyBytes = {}
    local json = decode(jsonCmd)
    local deviceSubType = json["deviceinfo"]["deviceSubType"]
    if (deviceSubType == 1) then end
    local query = json["query"]
    local control = json["control"]
    local status = json["status"]
    if (query) then
        if (query["query_type"] == "temperature") then
            uptable["isTemperatureQuery"] = true
        end
        bodyBytes[0] = 0x00
        infoM = getTotalMsg(bodyBytes, uptable["BYTE_MSG_TYPE_QUERY"])
    elseif (control) then
        if (status) then jsonToModel(status) end
        if (control) then jsonToModel(control) end
        local num = 119
        if (uptable["hexLength"] ~= nil) then num = uptable["hexLength"] end
        for i = 0, num do bodyBytes[i] = 0 end
        bodyBytes[0] = 0x00
        bodyBytes[1] = bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(bit.bor(bit.band(uptable["codeMode"], 0x01), bit.band(uptable["freezingMode"], 0x02)),
            bit.band(uptable["smartMode"], 0x04)), bit.band(uptable["energySavingMode"], 0x08)),
            bit.band(uptable["holidayMode"], 0x10)), bit.band(uptable["moisturizeMode"], 0x20)),
            bit.band(uptable["preservationMode"], 0x40)), bit.band(uptable["acmeFreezingMode"], 0x80))
        bodyBytes[2] = bit.bor(bit.lshift(bit.band(uptable["freezingTemperature"], 0x0F), 4),
            bit.band(uptable["refrigerationTemperature"], 0x0F))
        bodyBytes[3] = uptable["lVariableTemperature"]
        bodyBytes[4] = uptable["rVariableTemperature"]
        bodyBytes[5] = uptable["variableModeValue"]
        bodyBytes[6] = bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(bit.band(uptable["refrigerationPowerValue"], 0x01), bit.band(uptable["lVariablePowerValue"], 0x04)),
            bit.band(uptable["rVariablePowerValue"], 0x08)), bit.band(uptable["freezingPowerValue"], 0x10)),
            bit.band(uptable["crossPeakElectricityEnter"], 0x20)), bit.band(uptable["crossPeakElectricity"], 0x40)),
            bit.band(uptable["allRefrigerationPower"], 0x80))
        bodyBytes[7] = bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(bit.bor(bit.band(uptable["removeDew"], 0x01), bit.band(uptable["humidify"], 0x02)),
            bit.band(uptable["unfreeze"], 0x04)), bit.band(uptable["temperatureUnit"], 0x08)),
            bit.band(uptable["floodlight"], 0x10)), bit.band(uptable["functionSwitch"], 0xC0))
        bodyBytes[8] = bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(
        bit.bor(bit.bor(bit.band(uptable["radarMode"], 0x01), bit.band(uptable["milkMode"], 0x02)),
            bit.band(uptable["icedMode"], 0x04)), bit.band(uptable["plasmaAsepticMode"], 0x08)),
            bit.band(uptable["acquireIceaMode"], 0x10)), bit.band(uptable["brashIceaMode"], 0x20)),
            bit.band(uptable["acquireWaterMode"], 0x40)), bit.band(uptable["freezingIceMachinePower"], 0x80))
        bodyBytes[14] = bit.bor(bit.band(uptable["humanInduction"], 0x10),
            bit.band(uptable["humanInductionLightSwitch"], 0x40))
        bodyBytes[16] = bit.band(uptable["intervalRoomHumidityLevel"], 0xFE)
        if (num >= 25) then if (uptable["foodSite"] ~= nil) then bodyBytes[25] = bit.band(uptable["foodSite"], 0x0F) end end
        if (num >= 27) then if (uptable["microcrystalFresh"] ~= nil and uptable["dryZone"] ~= nil and uptable["performanceMode"] ~= nil and uptable["electronicSmell"] ~= nil and uptable["eradicatePesticideResidue"] ~= nil) then bodyBytes[27] =
                bit.bor(
                bit.bor(
                bit.bor(
                bit.bor(bit.bor(bit.band(uptable["microcrystalFresh"], 0x01), bit.band(uptable["dryZone"], 0x02)),
                    bit.band(uptable["electronicSmell"], 0x04)), bit.band(uptable["eradicatePesticideResidue"], 0x08)),
                    bit.band(uptable["humidity"], 0x70)), bit.band(uptable["performanceMode"], 0x80)) end end
        if (num >= 28) then if (uptable["normalTemperatureLevel"] ~= nil) then bodyBytes[28] = uptable
                ["normalTemperatureLevel"] end end
        if (num >= 29) then if (uptable["functionZoneLevel"] ~= nil) then bodyBytes[29] = uptable["functionZoneLevel"] end end
        if (num >= 30) then if (uptable["humiditySetting"] ~= nil and uptable["smartHumidity"] ~= nil) then bodyBytes[30] =
                bit.bor(bit.band(uptable["humiditySetting"], 0x7F), bit.band(uptable["smartHumidity"], 0x80)) end end
        if (num >= 31) then if (uptable["storageLeftDoorAuto"] ~= nil and uptable["storageRightDoorAuto"] ~= nil and uptable["freezerDoorAuto"] ~= nil and uptable["freezerDoorAutoControl"] ~= nil and uptable["storageDoorAutoControl"] ~= nil) then bodyBytes[31] =
                bit.bor(
                bit.bor(
                bit.bor(
                bit.bor(bit.band(uptable["storageLeftDoorAuto"], 0x03), bit.band(uptable["storageRightDoorAuto"], 0x0C)),
                    bit.band(uptable["freezerDoorAuto"], 0x30)), bit.band(uptable["freezerDoorAutoControl"], 0x40)),
                    bit.band(uptable["storageDoorAutoControl"], 0x80)) end end
        if (num >= 33) then if (uptable["storageIceMachinePower"] ~= nil and uptable["filterReplacementWarningElimination"] ~= nil) then bodyBytes[33] =
                bit.bor(bit.band(uptable["storageIceMachinePower"], 0x01),
                    bit.band(uptable["filterReplacementWarningElimination"], 0x80)) end end
        if (num >= 37) then
            bodyBytes[35] = uptable["storageFTemperature"]
            bodyBytes[36] = uptable["freezingFTemperature"]
            bodyBytes[37] = uptable["leftFlexzoneFTemperature"]
        end
        if (num >= 38) then if (uptable["electronicCleanStrong"] ~= nil) then bodyBytes[38] = bit.band(
                uptable["electronicCleanStrong"], 0x01) end end
        if (num >= 39) then if (uptable["quickBeverageTime"] ~= nil and uptable["quickBeverage"] ~= nil) then bodyBytes[39] =
                bit.bor(bit.band(uptable["quickBeverageTime"], 0x7F), bit.band(uptable["quickBeverage"], 0x80)) end end
        if (num >= 41) then
            if (uptable["aquaticProduct"] ~= nil and uptable["silentNightMode"] ~= nil and uptable["deepColdMode"] ~= nil) then bodyBytes[40] =
                bit.bor(
                bit.bor(
                bit.bor(bit.band(uptable["aquaticProduct"], 0x01), bit.band(uptable["silentNightMode"], 0x04)),
                    bit.band(uptable["deepColdMode"], 0x08)),
                    bit.bor(bit.band(uptable["vacuumMode"], 0x10), bit.band(uptable["vacuumCompleted"], 0x20))) end
            if (uptable["silentMode"] ~= nil) then bodyBytes[41] = bit.band(uptable["silentMode"], 0x08) end
        end
        if (num >= 42) then bodyBytes[42] = bit.bor(bit.band(uptable["storageLightLevel"], 0x1F),
                bit.band(uptable["nightMode"], 0x20)) end
        if (num >= 43) then if (uptable["voiceDoorAuto"] ~= nil and uptable["touchDoorAuto"] ~= nil and uptable["helpDoorAuto"] ~= nil and uptable["speedDoorOpen"] ~= nil and uptable["angleDoorOpen"] ~= nil and uptable["voiceAssistant"] ~= nil and uptable["noActionDoorClose"] ~= nil) then bodyBytes[43] =
                bit.bor(
                bit.bor(
                bit.bor(
                bit.bor(
                bit.bor(bit.bor(bit.band(uptable["voiceDoorAuto"], 0x01), bit.band(uptable["touchDoorAuto"], 0x02)),
                    bit.band(uptable["helpDoorAuto"], 0x04)), bit.band(uptable["speedDoorOpen"], 0x08)),
                    bit.band(uptable["angleDoorOpen"], 0x30)), bit.band(uptable["voiceAssistant"], 0x40)),
                    bit.band(uptable["noActionDoorClose"], 0x80)) end end
        if (num >= 44) then bodyBytes[44] = bit.bor(
            bit.bor(bit.bor(bit.band(uptable["foodExpireLight"], 0x08), bit.band(uptable["levelMsgLight"], 0x10)),
                bit.band(uptable["quickIceMode"], 0x20)), bit.band(uptable["noActionDoorCloseTime"], 0xC0)) end
        if (num >= 50) then
            bodyBytes[47] = uptable["beverageVialNumber"]
            bodyBytes[48] = uptable["beverageMidNumber"]
            bodyBytes[49] = uptable["beverageBigNumber"]
            bodyBytes[50] = uptable["beverageQuickTime"]
        end
        if (num >= 70) then
            bodyBytes[67] = bit.bor(bit.band(uptable["lightingEffect"], 0x07),
                bit.band(bit.lshift(uptable["lightingColor"], 3), 0xF8))
            bodyBytes[68] = uptable["customColorR"]
            bodyBytes[69] = uptable["customColorG"]
            bodyBytes[70] = uptable["customColorB"]
        end
        if (num >= 71) then bodyBytes[71] = bit.bor(bit.lshift(uptable["freezingLightOpen"], 6),
                bit.band(uptable["turnOffLight"], 0x01), bit.band(uptable["lightBrightness"], 0x02),
                bit.band(uptable["sunnyForSevenDays"], 0x04), bit.band(uptable["standbyMode"], 0x08),
                bit.band(uptable["quickFreezing"], 0x10), bit.band(uptable["freezingLightOpenChose"], 0x20)) end
        if (num >= 72) then bodyBytes[72] = uptable["wifiHumanInductionValue"] end
        if (num >= 73) then bodyBytes[73] = bit.bor(
            bit.bor(
            bit.bor(
            bit.bor(
            bit.bor(
            bit.bor(
            bit.bor(bit.band(uptable["teslaHandleSwitchMode"], 0x01), bit.band(uptable["fivePreservationMode"], 0x02)),
                bit.band(uptable["controlSugarFlag"], 0x04)), bit.band(uptable["strongControlSugarFlag"], 0x08)),
                bit.band(uptable["nightLightSwitch"], 0x10)), bit.band(uptable["openDoorTipsSwitch"], 0x20)),
                bit.band(uptable["pulseSwitch"], 0x40)), bit.band(uptable["deliveryMode"], 0x80)) end
        if (num >= 74) then bodyBytes[74] = bit.bor(bit.band(uptable["sabbathExitTime"], 0x3F),
                bit.band(uptable["sabbathMode"], 0xC0)) end
        if (num >= 77) then bodyBytes[77] = uptable["handleReturnTime"] end
        if (num >= 78) then bodyBytes[78] = bit.bor(bit.band(uptable["delayDefrostSwitch"], 0x01),
                bit.band(uptable["demandResponseSwitch"], 0x02), bit.band(uptable["temporaryDeloadingSwitch"], 0x04),
                bit.band(uptable["iceClean"], 0x08), bit.lshift(bit.band(uptable["deloadingMaximumExitTime"], 0x0F), 4)) end
        if (num >= 79) then bodyBytes[79] = bit.bor(bit.band(uptable["defrostMaximumExitTime"], 0x0F),
                bit.lshift(bit.band(uptable["demandResponseMaximumExitTime"], 0x0F), 4)) end
        if (num >= 80) then bodyBytes[80] = bit.bor(bit.band(uptable["telstarSavingMode"], 0x01),
                bit.band(uptable["panelDisplayGear"], 0x02), bit.band(uptable["offPeakDefrostSwitch"], 0x08),
                bit.lshift(bit.band(uptable["coolThresholdUpwardValue"], 0x03), 4),
                bit.lshift(bit.band(uptable["freezeThresholdUpwardValue"], 0x03), 6)) end
        if (num >= 81) then bodyBytes[81] = uptable["coolingTimeStartHour"] end
        if (num >= 82) then bodyBytes[82] = uptable["coolingTimeStartMinutes"] end
        if (num >= 83) then bodyBytes[83] = uptable["riseTimeStartHour"] end
        if (num >= 84) then bodyBytes[84] = uptable["riseTimeStartMinutes"] end
        if (num >= 85) then bodyBytes[85] = bit.bor(
            bit.lshift(bit.band(uptable["storageRightDoorAutoOpenAngle"], 0x0F), 4),
                bit.band(uptable["storageLeftDoorAutoOpenAngle"], 0x0F)) end
        if (num >= 86) then bodyBytes[86] = uptable["globalFlexTemperature"] end
        if (num >= 87) then bodyBytes[87] = bit.bor(
            bit.bor(
            bit.bor(
            bit.bor(bit.band(uptable["storageGlassDoorLight"], 0x07), bit.lshift(uptable["storageGlassDoorLightOpen"], 4)),
                bit.band(uptable["vegetableFreezing"], 0x40)), bit.band(uptable["vegetableFreezingDry"], 0x80)),
                bit.band(uptable["storageLightOpenChose"], 0x08)) end
        if (num >= 88) then bodyBytes[88] = bit.bor(
            bit.bor(bit.band(uptable["aiFruitDisplayControl"], 0x07), bit.band(uptable["aiFruitFlag"], 0x08)),
                bit.bor(bit.band(uptable["aiPurineDisplayControl"], 0x70), bit.band(uptable["aiPurineFlag"], 0x80))) end
        if (num >= 89) then bodyBytes[89] = bit.bor(bit.band(uptable["aiFruitBoxGear"], 0x07),
                bit.band(uptable["smartAiToSelfSelect"], 0x08), bit.band(uptable["aiPurine2ndEstimate"], 0x10),
                bit.band(uptable["surfaceLightModeSelect"], 0x20), bit.band(uptable["atmosphereLampModeSelect"], 0x40)) end
        if (num >= 90) then bodyBytes[90] = bit.bor(
            bit.bor(
            bit.bor(
            bit.bor(bit.bor(bit.band(uptable["storageDoorAutoOpen"], 0x01), bit.band(uptable["tapTap"], 0x02)),
                bit.lshift(bit.band(uptable["wineType"], 0x03), 2)),
                bit.lshift(bit.band(uptable["offlineVoiceSensitivity"], 0x03), 5)),
                bit.band(uptable["offlineVoiceSwitch"], 0x10)), bit.band(uptable["cameraSwitch"], 0x80)) end
        if (num >= 95) then
            bodyBytes[91] = bit.bor(bit.band(uptable["ledPwmDuty"], 0x7F), bit.band(uptable["sleepMode"], 0x80))
            bodyBytes[92] = bit.bor(
            bit.bor(
            bit.bor(bit.band(uptable["sleepModeStartHour"], 0x1F), bit.band(uptable["roomLedDimmingFlag"], 0x20)),
                bit.band(uptable["iceMachineStopIceFlag"], 0x40)), bit.band(uptable["displayBoardMuteFlag"], 0x80))
            bodyBytes[93] = bit.bor(bit.band(uptable["sleepModeStartMinute"], 0x3F),
                bit.band(uptable["electronicCleanSmartMode"], 0x40)); bodyBytes[94] = bit.band(
            uptable["sleepModeEndHour"], 0x1F)
            bodyBytes[95] = bit.band(uptable["sleepModeEndMinute"], 0x3F)
        end
        if (num >= 99) then
            bodyBytes[96] = bit.bor(
            bit.bor(bit.bor(bit.band(uptable["iceWaterMode"], 0x01), bit.band(uptable["smartRecommend"], 0x02)),
                bit.band(uptable["iceWaterMixType"], 0x08)),
                bit.bor(bit.lshift(bit.band(uptable["iceWaterMixProportion"], 0x03), 4),
                    bit.band(uptable["dividerSupportAutoFill"], 0x80)))
            bodyBytes[97] = bit.bor(
            bit.bor(bit.band(uptable["smartMorningStartHour"], 0x0F), bit.band(uptable["iceWaterMixTypeMorning"], 0x10)),
                bit.lshift(bit.band(uptable["iceWaterMixProportionMorning"], 0x03), 5))
            bodyBytes[98] = bit.bor(
            bit.bor(bit.band(uptable["smartNoonStartHour"], 0x0F), bit.band(uptable["iceWaterMixTypeNoon"], 0x10)),
                bit.lshift(bit.band(uptable["iceWaterMixProportionNoon"], 0x03), 5))
            bodyBytes[99] = bit.bor(
            bit.bor(bit.band(uptable["smartNightStartHour"], 0x0F), bit.band(uptable["iceWaterMixTypeNight"], 0x10)),
                bit.lshift(bit.band(uptable["iceWaterMixProportionNight"], 0x03), 5))
        end
        if (num >= 101) then
            bodyBytes[100] = uptable["openDoorWarningTime"]
            bodyBytes[101] = uptable["openDoorHoverTime"]
        end
        if (num >= 102) then bodyBytes[102] = bit.bor(
            bit.bor(
            bit.bor(bit.band(uptable["gpsReportSwitch"], 0x01), bit.band(uptable["freezerLightOneMinuteFlag"], 0x02)),
                bit.bor(bit.band(uptable["smartFreezeMode"], 0x04), bit.band(uptable["smartCoolMode"], 0x08))),
                bit.band(uptable["multiFuncZoneStatus"], 0x10)) end
        if (num >= 103) then bodyBytes[103] = bit.bor(bit.band(uptable["appSmartSelectionMode"], 0x01),
                bit.band(uptable["smartSelectionGearChange"], 0x02),
                bit.band(uptable["fridgeConstantTempHumidity"], 0x04)) end
        if (num >= 104) then if uptable["smartSelectionSetTemp"] == 99 then bodyBytes[104] = 0 else bodyBytes[104] =
                uptable["smartSelectionSetTemp"] end end
        if (num >= 105) then bodyBytes[105] = bit.band(uptable["tmfCoolFreezeMode"], 0x0F) end
        if (num >= 106) then bodyBytes[106] = bit.bor(bit.band(uptable["handleAtmosphereLampBrightness"], 0x0F),
                bit.lshift(bit.band(uptable["colmoCoolFreezeMode"], 0x03), 4)) end
        if (num >= 110) then bodyBytes[110] = bit.bor(bit.band(uptable["defrostModeSwitch"], 0x01),
                bit.band(uptable["defrostCompletedState"], 0x02),
                bit.lshift(bit.band(uptable["defrostRemainTimeData110"], 0xFF), 2)) end
        if (num >= 111) then bodyBytes[111] = uptable["defrostRemainTimeData111"] end
        if (num >= 112) then bodyBytes[112] = uptable["defrostTimeUserDefined"] end
        if (num >= 113) then bodyBytes[113] = bit.band(uptable["nfcSignalBoardEnabled"], 0x01) end
        if (num >= 117) then
            bodyBytes[116] = bit.bor(uptable["foodClipData116"], 0x00)
            bodyBytes[117] = bit.bor(uptable["foodClipData117"], 0x00)
        end
        if (num >= 118) then bodyBytes[118] = uptable["wifiHumanInductionFarValue"] end
        if (num >= 119) then bodyBytes[119] = uptable["wifiHumanInductionExistValue"] end
        if (num >= 120) then bodyBytes[120] = uptable["rangeTrackingShortValue"] end
        if (num >= 121) then bodyBytes[121] = uptable["rangeTrackingFarValue"] end
        if (num >= 122) then bodyBytes[122] = uptable["resistSpectrumSymmetryDisturbRatio"] end
        if (num >= 123) then bodyBytes[123] = uptable["resistSpectrumSymmetryDisturbNum"] end
        if (num >= 124) then bodyBytes[124] = uptable["aiHumanInductionSimilarityValue"] end
        if (num >= 131) then bodyBytes[131] = bit.band(uptable["basicPowerSavingSwitch"], 0x01) end
        if (num >= 132) then bodyBytes[132] = uptable["internalDeloadingMaximumExitTime"] end
        if (num >= 133) then bodyBytes[133] = uptable["smartDenoiseOpenHours"] end
        if (num >= 134) then bodyBytes[134] = uptable["smartDenoiseOpenMins"] end
        if (num >= 135) then bodyBytes[135] = bit.bor(bit.band(uptable["freezerElecPowerfulDeodorizeSwitch"], 0x01),
                bit.lshift(bit.band(uptable["freezerElecPowerfulDeodorizeHourTime"], 0xFE), 1)) end
        if (num >= 136) then bodyBytes[136] = uptable["freezerElecPowerfulDeodorizeMinTime"] end
        if (num >= 137) then bodyBytes[137] = uptable["storageElecPowerfulDeodorizeHourTime"] end
        infoM = getTotalMsg(bodyBytes, uptable["BYTE_MSG_TYPE_CONTROL"])
    end
    local ret = table2string(infoM)
    ret = string2hexstring(ret)
    return ret
end

function dataToJson(jsonCmd)
    if (not jsonCmd) then return nil end
    local json = decode(jsonCmd)
    local deviceinfo = json["deviceinfo"]
    local deviceSubType = deviceinfo["deviceSubtype"]
    if (deviceSubType == 1) then end
    local status = json["status"]
    if (status) then jsonToModel(status) end
    local binData = json["msg"]["data"]
    local info = {}
    local msgBytes = {}
    local bodyBytes = {}
    local msgLength = 0
    local bodyLength = 0
    info = string2table(binData)
    uptable["dataType"] = info[10]; uptable["hexLength"] = info[2]; for i = 1, #info do msgBytes[i - 1] = info[i] end
    msgLength = msgBytes[1]
    bodyLength = msgLength - uptable["BYTE_PROTOCOL_HEAD_LENGTH"] - 1
    for i = 0, bodyLength do bodyBytes[i] = msgBytes[i + uptable["BYTE_PROTOCOL_HEAD_LENGTH"]] end
    binToModel(bodyBytes)
    local streams = {}
    streams[uptable["KEY_VERSION"]] = uptable["VALUE_VERSION"]
    if (uptable["isTemperatureQuery"]) then
        streams["refrigeration_real_temperature"] = int2String(math.floor((uptable["refrigerationRealTemperature"] - 100) / 2))
        streams["freezing_real_temperature"] = int2String(math.floor((uptable["freezingRealTemperature"] - 100) / 2))
        streams["left_variable_real_temperature"] = int2String(math.floor((uptable["lVariableRealTemperature"] - 100) / 2))
        streams["right_variable_real_temperature"] = int2String(math.floor((uptable["rVariableRealTemperature"] - 100) / 2))
        uptable["isTemperatureQuery"] = false
    elseif ((uptable["dataType"] == 0x02 and bodyBytes[0] == 0x00) or (uptable["dataType"] == 0x03 and bodyBytes[0] == 0x00) or (uptable["dataType"] == 0x04 and bodyBytes[0] == 0x02)) then
        streams["hex_length"] = uptable["hexLength"] - 11
        if (uptable["codeMode"] == 0x01) then streams["storage_mode"] = "on" elseif (uptable["codeMode"] == 0x00) then streams["storage_mode"] =
            "off" end
        if (uptable["freezingMode"] == 0x02) then streams["freezing_mode"] = "on" elseif (uptable["freezingMode"] == 0x00) then streams["freezing_mode"] =
            "off" end
        if (uptable["smartMode"] == 0x04) then streams["intelligent_mode"] = "on" elseif (uptable["smartMode"] == 0x00) then streams["intelligent_mode"] =
            "off" end
        if (uptable["energySavingMode"] == 0x08) then streams["energy_saving_mode"] = "on" elseif (uptable["energySavingMode"] == 0x00) then streams["energy_saving_mode"] =
            "off" end
        if (uptable["holidayMode"] == 0x10) then streams["holiday_mode"] = "on" elseif (uptable["holidayMode"] == 0x00) then streams["holiday_mode"] =
            "off" end
        if (uptable["moisturizeMode"] == 0x20) then streams["moisturize_mode"] = "on" elseif (uptable["moisturizeMode"] == 0x00) then streams["moisturize_mode"] =
            "off" end
        if (uptable["preservationMode"] == 0x40) then streams["preservation_mode"] = "on" elseif (uptable["preservationMode"] == 0x00) then streams["preservation_mode"] =
            "off" end
        if (uptable["acmeFreezingMode"] == 0x80) then streams["acme_freezing_mode"] = "on" elseif (uptable["acmeFreezingMode"] == 0x00) then streams["acme_freezing_mode"] =
            "off" end
        if (uptable["colmoCoolFreezeMode"] == 0x00) then
            streams["storage_temperature"] = int2String(uptable["refrigerationTemperature"])
            streams["freezing_temperature"] = int2String(-12 - uptable["freezingTemperature"])
        elseif (uptable["colmoCoolFreezeMode"] == 0x01) then
            streams["storage_temperature"] = int2String(uptable["refrigerationTemperature"])
            streams["freezing_temperature"] = int2String(uptable["freezingTemperature"] - 3)
        elseif (uptable["colmoCoolFreezeMode"] == 0x02) then
            streams["storage_temperature"] = int2String(-11 - uptable["refrigerationTemperature"])
            streams["freezing_temperature"] = int2String(-12 - uptable["freezingTemperature"])
        elseif (uptable["colmoCoolFreezeMode"] == 0x03) then
            streams["storage_temperature"] = int2String(uptable["refrigerationTemperature"])
            streams["freezing_temperature"] = int2String(-12 - uptable["freezingTemperature"])
        end
        if ((uptable["lVariableTemperature"] >= 1) and (uptable["lVariableTemperature"] <= 29)) then streams["left_flexzone_temperature"] =
            int2String(uptable["lVariableTemperature"] - 19) elseif ((uptable["lVariableTemperature"] >= 49) and (uptable["lVariableTemperature"] <= 54)) then streams["left_flexzone_temperature"] =
            int2String(30 - uptable["lVariableTemperature"]) else streams["left_flexzone_temperature"] = "0" end
        if ((uptable["rVariableTemperature"] >= 1) and (uptable["rVariableTemperature"] <= 29)) then streams["right_flexzone_temperature"] =
            int2String(uptable["rVariableTemperature"] - 19) elseif ((uptable["rVariableTemperature"] >= 49) and (uptable["rVariableTemperature"] <= 54)) then streams["right_flexzone_temperature"] =
            int2String(30 - uptable["rVariableTemperature"]) else streams["right_flexzone_temperature"] = "0" end
        if (uptable["variableModeValue"] == 0x01) then streams["variable_mode"] = "soft_freezing_mode" elseif (uptable["variableModeValue"] == 0x00) then streams["variable_mode"] =
            "none_mode" elseif (uptable["variableModeValue"] == 0x02) then streams["variable_mode"] = "zero_fresh_mode" elseif (uptable["variableModeValue"] == 0x03) then streams["variable_mode"] =
            "cold_drink_mode" elseif (uptable["variableModeValue"] == 0x04) then streams["variable_mode"] =
            "fresh_product_mode" elseif (uptable["variableModeValue"] == 0x05) then streams["variable_mode"] =
            "partial_freezing_mode" elseif (uptable["variableModeValue"] == 0x06) then streams["variable_mode"] =
            "dry_zone_mode" elseif (uptable["variableModeValue"] == 0x07) then streams["variable_mode"] =
            "freeze_warm_mode" elseif (uptable["variableModeValue"] == 0x08) then streams["variable_mode"] =
            "freeze_mode" end
        if (uptable["refrigerationPowerValue"] == 0x00) then streams["storage_power"] = "on" elseif (uptable["refrigerationPowerValue"] == 0x01) then streams["storage_power"] =
            "off" end
        if (uptable["lVariablePowerValue"] == 0x00) then streams["left_flexzone_power"] = "on" elseif (uptable["lVariablePowerValue"] == 0x04) then streams["left_flexzone_power"] =
            "off" end
        if (uptable["rVariablePowerValue"] == 0x00) then streams["right_flexzone_power"] = "on" elseif (uptable["rVariablePowerValue"] == 0x08) then streams["right_flexzone_power"] =
            "off" end
        if (uptable["freezingPowerValue"] == 0x00) then streams["freezing_power"] = "on" elseif (uptable["freezingPowerValue"] == 0x10) then streams["freezing_power"] =
            "off" end
        if (uptable["crossPeakElectricityEnter"] == 0x20) then streams["cross_peak_electricity_enter"] = "enter" elseif (uptable["crossPeakElectricityEnter"] == 0x00) then streams["cross_peak_electricity_enter"] =
            "quit" end
        if (uptable["crossPeakElectricity"] == 0x40) then streams["cross_peak_electricity"] = "on" elseif (uptable["crossPeakElectricity"] == 0x00) then streams["cross_peak_electricity"] =
            "off" end
        if (uptable["allRefrigerationPower"] == 0x80) then streams["all_refrigeration_power"] = "on" elseif (uptable["allRefrigerationPower"] == 0x00) then streams["all_refrigeration_power"] =
            "off" end
        if (uptable["removeDew"] == 0x01) then streams["remove_dew_power"] = "on" elseif (uptable["removeDew"] == 0x00) then streams["remove_dew_power"] =
            "off" end
        if (uptable["humidify"] == 0x02) then streams["humidify_power"] = "on" elseif (uptable["humidify"] == 0x00) then streams["humidify_power"] =
            "off" end
        if (uptable["unfreeze"] == 0x04) then streams["unfreeze_power"] = "on" elseif (uptable["unfreeze"] == 0x00) then streams["unfreeze_power"] =
            "off" end
        if (uptable["temperatureUnit"] == 0x08) then streams["temperature_unit"] = "fahrenheit" elseif (uptable["temperatureUnit"] == 0x00) then streams["temperature_unit"] =
            "celsius" end
        if (uptable["floodlight"] == 0x10) then streams["floodlight_power"] = "on" elseif (uptable["floodlight"] == 0x00) then streams["floodlight_power"] =
            "off" end
        if (uptable["functionSwitch"] == 0x00) then streams["icea_bar_function_switch"] = "default" elseif (uptable["functionSwitch"] == 0x40) then streams["icea_bar_function_switch"] =
            "refrigeration" elseif (uptable["functionSwitch"] == 0x80) then streams["icea_bar_function_switch"] =
            "freezing" end
        if (uptable["radarMode"] == 0x01) then streams["radar_mode_power"] = "on" elseif (uptable["radarMode"] == 0x00) then streams["radar_mode_power"] =
            "off" end
        if (uptable["milkMode"] == 0x02) then streams["milk_mode_power"] = "on" elseif (uptable["milkMode"] == 0x00) then streams["milk_mode_power"] =
            "off" end
        if (uptable["icedMode"] == 0x04) then streams["icea_mode_power"] = "on" elseif (uptable["icedMode"] == 0x00) then streams["icea_mode_power"] =
            "off" end
        if (uptable["plasmaAsepticMode"] == 0x08) then streams["plasma_aseptic_mode_power"] = "on" elseif (uptable["plasmaAsepticMode"] == 0x00) then streams["plasma_aseptic_mode_power"] =
            "off" end
        if (uptable["acquireIceaMode"] == 0x10) then streams["acquire_icea_mode_power"] = "on" elseif (uptable["acquireIceaMode"] == 0x00) then streams["acquire_icea_mode_power"] =
            "off" end
        if (uptable["brashIceaMode"] == 0x20) then streams["brash_icea_mode_power"] = "on" elseif (uptable["brashIceaMode"] == 0x00) then streams["brash_icea_mode_power"] =
            "off" end
        if (uptable["acquireWaterMode"] == 0x40) then streams["acquire_water_mode_power"] = "on" elseif (uptable["acquireWaterMode"] == 0x00) then streams["acquire_water_mode_power"] =
            "off" end
        if (uptable["freezingIceMachinePower"] == 0x80) then streams["freezing_ice_machine_power"] = "on" elseif (uptable["freezingIceMachinePower"] == 0x00) then streams["freezing_ice_machine_power"] =
            "off" end
        streams["freeze_fahrenheit_level"] = int2String(uptable["freezingFahrenheit"])
        streams["refrigeration_fahrenheit_level"] = int2String(uptable["refrigerationFahrenheit"])
        streams["leach_expire_day"] = int2String(uptable["leachExpireDay"])
        streams["power_consumption_low"] = int2String(uptable["powerConsumptionLow"])
        streams["power_consumption_high"] = int2String(uptable["powerConsumptionHigh"])
        if (uptable["freezingMotorResetStatus"] == 0x01) then streams["freezing_motor_reset_status"] = "valid" elseif (uptable["freezingMotorResetStatus"] == 0x00) then streams["freezing_motor_reset_status"] =
            "invalid" end
        if (uptable["freezingMotorDeicingStatus"] == 0x02) then streams["freezing_motor_deicing_status"] = "valid" elseif (uptable["freezingMotorDeicingStatus"] == 0x00) then streams["freezing_motor_deicing_status"] =
            "invalid" end
        if (uptable["freezingIceMachineWaterStatus"] == 0x04) then streams["freezing_ice_machine_water_status"] = "valid" elseif (uptable["freezingIceMachineWaterStatus"] == 0x00) then streams["freezing_ice_machine_water_status"] =
            "invalid" end
        if (uptable["freezingAllIceStatus"] == 0x08) then streams["freezing_all_ice_status"] = "valid" elseif (uptable["freezingAllIceStatus"] == 0x00) then streams["freezing_all_ice_status"] =
            "invalid" end
        if (uptable["humanInduction"] == 0x10) then streams["human_induction_status"] = "valid" elseif (uptable["humanInduction"] == 0x00) then streams["human_induction_status"] =
            "invalid" end
        if (uptable["freezerIcemakerWaterShortage"] == 0x20) then streams["freezer_icemaker_water_shortage"] = "shortage" elseif (uptable["freezerIcemakerWaterShortage"] == 0x00) then streams["freezer_icemaker_water_shortage"] =
            "normal" end
        if (uptable["humanInductionLightSwitch"] == 0x40) then streams["human_induction_light_switch"] = "on" elseif (uptable["humanInductionLightSwitch"] == 0x00) then streams["human_induction_light_switch"] =
            "off" end
        if (uptable["refrigerationDoorPower"] == 0x01) then streams["storage_door_state"] = "on" elseif (uptable["refrigerationDoorPower"] == 0x00) then streams["storage_door_state"] =
            "off" end
        if (uptable["freezingDoorPower"] == 0x02) then streams["freezer_door_state"] = "on" elseif (uptable["freezingDoorPower"] == 0x00) then streams["freezer_door_state"] =
            "off" end
        if (uptable["variableDoorPower"] == 0x04) then streams["flexzone_door_state"] = "on" elseif (uptable["variableDoorPower"] == 0x00) then streams["flexzone_door_state"] =
            "off" end
        if (uptable["iceMouthPower"] == 0x08) then streams["ice_mouth_power"] = "on" elseif (uptable["iceMouthPower"] == 0x00) then streams["ice_mouth_power"] =
            "off" end
        if (uptable["barDoorPower"] == 0x10) then streams["bar_door_state"] = "on" elseif (uptable["barDoorPower"] == 0x00) then streams["bar_door_state"] =
            "off" end
        if (uptable["storageIceHomeDoorState"] == 0x20) then streams["storage_ice_home_door_state"] = "on" elseif (uptable["storageIceHomeDoorState"] == 0x00) then streams["storage_ice_home_door_state"] =
            "off" end
        if (uptable["isHaveFreezingIce"] == 0x40) then streams["is_have_freezing_ice"] = "yes" elseif (uptable["isHaveFreezingIce"] == 0x00) then streams["is_have_freezing_ice"] =
            "no" end
        if (uptable["isError"] == 0x01) then streams["is_error"] = "yes" elseif (uptable["isError"] == 0x00) then streams["is_error"] =
            "no" end
        streams["interval_room_humidity_level"] = int2String(uptable["intervalRoomHumidityLevel"])
        streams["refrigeration_real_temperature"] = int2String(math.floor((uptable["refrigerationRealTemperature"] - 100) /
        2))
        streams["freezing_real_temperature"] = int2String(math.floor((uptable["freezingRealTemperature"] - 100) / 2))
        streams["left_variable_real_temperature"] = int2String(math.floor((uptable["lVariableRealTemperature"] - 100) / 2))
        streams["right_variable_real_temperature"] = int2String(math.floor((uptable["rVariableRealTemperature"] - 100) /
        2))
        if (bodyLength > 22) then
            streams["fast_cold_minute"] = int2String(256 * uptable["fastColdMinuteHigh"] + uptable["fastColdMinuteLow"])
            streams["intake_value_opened_num_high"] = int2String(uptable["fastColdMinuteLow"])
            streams["intake_value_opened_num_low"] = int2String(uptable["fastColdMinuteHigh"])
        end
        if (bodyLength > 24) then
            streams["fast_freeze_minute"] = int2String(256 * uptable["fastFreezeMinuteLow"] +
            uptable["fastFreezeMinuteHigh"])
            streams["total_ice_making_num_high"] = int2String(uptable["fastFreezeMinuteLow"])
            streams["total_ice_making_num_low"] = int2String(uptable["fastFreezeMinuteHigh"])
        end
        if (bodyLength > 25) then
            if (uptable["foodSite"] == 0x00) then streams["food_site"] = "left_freezing_room" elseif (uptable["foodSite"] == 0x01) then streams["food_site"] =
                "right_freezing_room" end
            if (uptable["beef"] == 0x40) then streams["beef"] = "exist" elseif (uptable["foodSite"] == 0x00) then streams["beef"] =
                "nonexistence" end
            if (uptable["pork"] == 0x80) then streams["pork"] = "exist" elseif (uptable["pork"] == 0x00) then streams["pork"] =
                "nonexistence" end
            if (uptable["mutton"] == 0x01) then streams["mutton"] = "exist" elseif (uptable["mutton"] == 0x00) then streams["mutton"] =
                "nonexistence" end
            if (uptable["chicken"] == 0x02) then streams["chicken"] = "exist" elseif (uptable["chicken"] == 0x00) then streams["chicken"] =
                "nonexistence" end
            if (uptable["duckMeat"] == 0x04) then streams["duck_meat"] = "exist" elseif (uptable["duckMeat"] == 0x00) then streams["duck_meat"] =
                "nonexistence" end
            if (uptable["fish"] == 0x08) then streams["fish"] = "exist" elseif (uptable["fish"] == 0x00) then streams["fish"] =
                "nonexistence" end
            if (uptable["shrimp"] == 0x10) then streams["shrimp"] = "exist" elseif (uptable["shrimp"] == 0x00) then streams["shrimp"] =
                "nonexistence" end
            if (uptable["dumplings"] == 0x20) then streams["dumplings"] = "exist" elseif (uptable["dumplings"] == 0x00) then streams["dumplings"] =
                "nonexistence" end
            if (uptable["gluePudding"] == 0x40) then streams["gluepudding"] = "exist" elseif (uptable["gluePudding"] == 0x00) then streams["gluepudding"] =
                "nonexistence" end
            if (uptable["iceCream"] == 0x80) then streams["ice_cream"] = "exist" elseif (uptable["iceCream"] == 0x00) then streams["ice_cream"] =
                "nonexistence" end
            if (uptable["microcrystalFresh"] == 0x01) then streams["microcrystal_fresh"] = "on" elseif (uptable["microcrystalFresh"] == 0x00) then streams["microcrystal_fresh"] =
                "off" end
            if (uptable["dryZone"] == 0x02) then streams["dry_zone"] = "on" elseif (uptable["dryZone"] == 0x00) then streams["dry_zone"] =
                "off" end
            if (uptable["electronicSmell"] == 0x04) then streams["electronic_smell"] = "on" elseif (uptable["electronicSmell"] == 0x00) then streams["electronic_smell"] =
                "off" end
            if (uptable["eradicatePesticideResidue"] == 0x08) then streams["eradicate_pesticide_residue"] = "on" elseif (uptable["eradicatePesticideResidue"] == 0x00) then streams["eradicate_pesticide_residue"] =
                "off" end
            if (uptable["humidity"] == 0x10) then streams["humidity"] = "high" elseif (uptable["humidity"] == 0x20) then streams["humidity"] =
                "low" end
            if (uptable["performanceMode"] == 0x80) then streams["performance_mode"] = "on" elseif (uptable["performanceMode"] == 0x00) then streams["performance_mode"] =
                "off" end
            streams["normal_zone_level"] = int2String(uptable["normalTemperatureLevel"])
            streams["function_zone_level"] = int2String(uptable["functionZoneLevel"])
            if (bodyLength > 30) then
                streams["humidify_setting"] = int2String(uptable["humiditySetting"])
                if (uptable["smartHumidity"] == 0x80) then streams["smart_humidify"] = "on" elseif (uptable["smartHumidity"] == 0x00) then streams["smart_humidify"] =
                    "off" end
                if (bodyLength > 31) then
                    if (uptable["storageLeftDoorAuto"] == 0x01) then streams["storage_left_door_auto"] = "on" elseif (uptable["storageLeftDoorAuto"] == 0x02) then streams["storage_left_door_auto"] =
                        "off" elseif (uptable["storageLeftDoorAuto"] == 0x00) then streams["storage_left_door_auto"] =
                        "invalid" end
                    if (uptable["storageRightDoorAuto"] == 0x04) then streams["storage_right_door_auto"] = "on" elseif (uptable["storageRightDoorAuto"] == 0x08) then streams["storage_right_door_auto"] =
                        "off" elseif (uptable["storageRightDoorAuto"] == 0x00) then streams["storage_right_door_auto"] =
                        "invalid" end
                    if (uptable["freezerDoorAuto"] == 0x10) then streams["freezer_door_auto"] = "on" elseif (uptable["freezerDoorAuto"] == 0x20) then streams["freezer_door_auto"] =
                        "off" elseif (uptable["freezerDoorAuto"] == 0x00) then streams["freezer_door_auto"] = "invalid" end
                    if (uptable["freezerDoorAutoControl"] == 0x40) then streams["freezer_door_auto_control"] = "on" elseif (uptable["freezerDoorAutoControl"] == 0x00) then streams["freezer_door_auto_control"] =
                        "off" end
                    if (uptable["storageDoorAutoControl"] == 0x80) then streams["storage_door_auto_control"] = "on" elseif (uptable["storageDoorAutoControl"] == 0x00) then streams["storage_door_auto_control"] =
                        "off" end
                    streams["eradicate_pesticide_residue_progress"] = int2String(uptable
                    ["eradicatePesticideResidueProgress"])
                    if (uptable["eradicatePesticideResidueCompletion"] == 0x80) then streams["eradicate_pesticide_residue_completion"] =
                        "yes" elseif (uptable["eradicatePesticideResidueCompletion"] == 0x00) then streams["eradicate_pesticide_residue_completion"] =
                        "no" end
                    if (bodyLength > 33) then
                        if (uptable["storageIceMachinePower"] == 0x01) then streams["storage_ice_machine_power"] = "on" elseif (uptable["storageIceMachinePower"] == 0x00) then streams["storage_ice_machine_power"] =
                            "off" end
                        if (uptable["storageMotorResetStatus"] == 0x02) then streams["storage_motor_reset_status"] =
                            "valid" elseif (uptable["storageMotorResetStatus"] == 0x00) then streams["storage_motor_reset_status"] =
                            "invalid" end
                        if (uptable["storageMotorDeicingStatus"] == 0x04) then streams["storage_motor_deicing_status"] =
                            "valid" elseif (uptable["storageMotorDeicingStatus"] == 0x00) then streams["storage_motor_deicing_status"] =
                            "invalid" end
                        if (uptable["storageIceMachineWaterStatus"] == 0x08) then streams["storage_ice_machine_water_status"] =
                            "valid" elseif (uptable["storageIceMachineWaterStatus"] == 0x00) then streams["storage_ice_machine_water_status"] =
                            "invalid" end
                        if (uptable["storageAllIceStatus"] == 0x10) then streams["storage_all_ice_status"] = "valid" elseif (uptable["storageAllIceStatus"] == 0x00) then streams["storage_all_ice_status"] =
                            "invalid" end
                        if (uptable["filterExpiresMildWarning"] == 0x20) then streams["filter_expires_mild_warning"] =
                            "valid" elseif (uptable["filterExpiresMildWarning"] == 0x00) then streams["filter_expires_mild_warning"] =
                            "invalid" end
                        if (uptable["filterExpiresSevereWarning"] == 0x40) then streams["filter_expires_severe_warning"] =
                            "valid" elseif (uptable["filterExpiresSevereWarning"] == 0x00) then streams["filter_expires_severe_warning"] =
                            "invalid" end
                        streams["ice_room_real_temperature"] = int2String(math.floor((uptable["iceRoomRealTemperature"] - 100) /
                        2))
                        if (bodyLength > 35) then
                            streams["storage_F_temperature"] = int2String(uptable["storageFTemperature"])
                            streams["freezing_F_temperature"] = int2String(11 - uptable["freezingFTemperature"])
                            streams["left_flexzone_F_temperature"] = int2String(uptable["leftFlexzoneFTemperature"] - 1)
                            if (bodyLength > 38) then
                                if (uptable["electronicCleanStrong"] == 0x01) then streams["electronic_clean_strong"] =
                                    "on" elseif (uptable["electronicCleanStrong"] == 0x00) then streams["electronic_clean_strong"] =
                                    "off" end
                                streams["electronic_clean_timeout"] = int2String(uptable["electronicCleanTimeout"])
                                if (bodyLength > 39) then
                                    streams["quick_beverage_time"] = int2String(uptable["quickBeverageTime"])
                                    if (uptable["quickBeverage"] == 0x80) then streams["quick_beverage"] = "on" elseif (uptable["quickBeverage"] == 0x00) then streams["quick_beverage"] =
                                        "off" end
                                    if (bodyLength > 40) then
                                        if (uptable["aquaticProduct"] == 0x01) then streams["aquatic_product"] = "on" elseif (uptable["aquaticProduct"] == 0x00) then streams["aquatic_product"] =
                                            "off" end
                                        if (uptable["silentNightMode"] == 0x04) then streams["silent_night_mode"] = "on" elseif (uptable["silentNightMode"] == 0x00) then streams["silent_night_mode"] =
                                            "off" end
                                        if (uptable["silentMode"] == 0x08) then streams["silent_mode"] = "on" elseif (uptable["silentMode"] == 0x00) then streams["silent_mode"] =
                                            "off" end
                                        if (uptable["deepColdMode"] == 0x08) then streams["deep_cold_mode"] = "on" elseif (uptable["deepColdMode"] == 0x00) then streams["deep_cold_mode"] =
                                            "off" end
                                        if (uptable["vacuumMode"] == 0x10) then streams["vacuum_mode"] = "on" elseif (uptable["vacuumMode"] == 0x00) then streams["vacuum_mode"] =
                                            "off" end
                                        if (uptable["vacuumCompleted"] == 0x20) then streams["vacuum_completed"] = "yes" elseif (uptable["vacuumCompleted"] == 0x00) then streams["vacuum_completed"] =
                                            "no" end
                                        if (uptable["blueRayMode"] == 0x02) then streams["blue_ray_mode"] = "on" elseif (uptable["blueRayMode"] == 0x00) then streams["blue_ray_mode"] =
                                            "off" end
                                        if (uptable["flexDoorAuto"] == 0x10) then streams["flex_door_auto"] = "on" elseif (uptable["flexDoorAuto"] == 0x20) then streams["flex_door_auto"] =
                                            "off" elseif (uptable["flexDoorAuto"] == 0x00) then streams["flex_door_auto"] =
                                            "invalid" end
                                        if (uptable["freezerDownDoorAuto"] == 0x40) then streams["freezer_down_door_auto"] =
                                            "on" elseif (uptable["freezerDownDoorAuto"] == 0x80) then streams["freezer_down_door_auto"] =
                                            "off" elseif (uptable["freezerDownDoorAuto"] == 0x00) then streams["freezer_down_door_auto"] =
                                            "invalid" end
                                        if (bodyLength > 42) then
                                            streams["storage_light_level"] = int2String(uptable["storageLightLevel"])
                                            if (uptable["nightMode"] == 0x20) then streams["night_mode"] = "on" elseif (uptable["nightMode"] == 0x00) then streams["night_mode"] =
                                                "off" end
                                            if (uptable["quickBeverageCompleted"] == 0x40) then streams["quick_beverage_completed"] =
                                                "yes" elseif (uptable["quickBeverageCompleted"] == 0x00) then streams["quick_beverage_completed"] =
                                                "no" end
                                            if (uptable["voiceDoorAuto"] == 0x01) then streams["voice_door_auto"] = "on" elseif (uptable["voiceDoorAuto"] == 0x00) then streams["voice_door_auto"] =
                                                "off" end
                                            if (uptable["touchDoorAuto"] == 0x02) then streams["touch_door_auto"] = "on" elseif (uptable["touchDoorAuto"] == 0x00) then streams["touch_door_auto"] =
                                                "off" end
                                            if (uptable["helpDoorAuto"] == 0x04) then streams["help_door_auto"] = "on" elseif (uptable["helpDoorAuto"] == 0x00) then streams["help_door_auto"] =
                                                "off" end
                                            if (uptable["speedDoorOpen"] == 0x08) then streams["speed_door_open"] =
                                                "fast" elseif (uptable["speedDoorOpen"] == 0x00) then streams["speed_door_open"] =
                                                "slow" end
                                            if (uptable["angleDoorOpen"] == 0x20) then streams["angle_door_open"] =
                                                int2String("110") elseif (uptable["angleDoorOpen"] == 0x10) then streams["angle_door_open"] =
                                                int2String("90") elseif (uptable["angleDoorOpen"] == 0x30) then streams["angle_door_open"] =
                                                int2String("135") end
                                            if (uptable["voiceAssistant"] == 0x40) then streams["voice_assistant"] = "on" elseif (uptable["voiceAssistant"] == 0x00) then streams["voice_assistant"] =
                                                "off" end
                                            if (uptable["noActionDoorClose"] == 0x80) then streams["no_action_door_close"] =
                                                "on" elseif (uptable["noActionDoorClose"] == 0x00) then streams["no_action_door_close"] =
                                                "off" end
                                            if (uptable["foodExpireLight"] == 0x08) then streams["food_expire_light"] =
                                                "on" elseif (uptable["foodExpireLight"] == 0x00) then streams["food_expire_light"] =
                                                "off" end
                                            if (uptable["levelMsgLight"] == 0x10) then streams["level_msg_light"] = "on" elseif (uptable["levelMsgLight"] == 0x00) then streams["level_msg_light"] =
                                                "off" end
                                            if (uptable["quickIceMode"] == 0x20) then streams["rapid_ice_making"] = "on" elseif (uptable["quickIceMode"] == 0x00) then streams["rapid_ice_making"] =
                                                "off" end
                                            if (uptable["noActionDoorCloseTime"] == 0x00) then streams["no_action_door_close_time"] =
                                                int2String("60") elseif (uptable["noActionDoorCloseTime"] == 0x40) then streams["no_action_door_close_time"] =
                                                int2String("45") elseif (uptable["noActionDoorCloseTime"] == 0x80) then streams["no_action_door_close_time"] =
                                                int2String("30") end
                                            if (bodyLength >= 45) then
                                                streams["leach_expire_day_high"] = int2String(uptable
                                                ["leachExpireDayHigh"])
                                                streams["filter_natural_time_high"] = int2String(uptable
                                                ["filterNaturalTimeHigh"])
                                                streams["filter_natural_time_low"] = int2String(uptable
                                                ["filterNaturalTimeLow"])
                                                streams["water_flow_percentage"] = int2String(uptable
                                                ["waterFlowPercentage"])
                                                if (bodyLength >= 47) then
                                                    streams["beverage_vial_number"] = int2String(uptable
                                                    ["beverageVialNumber"])
                                                    streams["beverage_mid_number"] = int2String(uptable
                                                    ["beverageMidNumber"])
                                                    streams["beverage_big_number"] = int2String(uptable
                                                    ["beverageBigNumber"])
                                                    streams["beverage_quick_time"] = int2String(uptable
                                                    ["beverageQuickTime"])
                                                    if (bodyLength >= 51) then
                                                        streams["local_time_hour"] = int2String(uptable["localTimeHour"])
                                                        streams["local_time_minute"] = int2String(uptable
                                                        ["localTimeMinute"])
                                                        streams["local_time_second"] = int2String(uptable
                                                        ["localTimeSecond"])
                                                        streams["time_zone"] = int2String(uptable["timeZone"])
                                                        streams["week"] = int2String(uptable["week"])
                                                        streams["day"] = int2String(uptable["day"])
                                                        streams["month"] = int2String(uptable["month"])
                                                        streams["year"] = int2String(uptable["year"])
                                                        if (bodyLength >= 59) then
                                                            streams["e_cleaning_percentage"] = int2String(uptable
                                                            ["eCleaningPercentage"])
                                                            streams["drink_valve_equal_open_high"] = int2String(uptable
                                                            ["drinkValveEqualOpenHigh"])
                                                            streams["drink_valve_equal_open_low"] = int2String(uptable
                                                            ["drinkValveEqualOpenLow"])
                                                            streams["inlet_valve_equal_open_high"] = int2String(uptable
                                                            ["inletValveEqualOpenHigh"])
                                                            streams["inlet_valve_equal_open_low"] = int2String(uptable
                                                            ["inletValveEqualOpenLow"])
                                                            streams["filter_element_use_percentage"] = int2String(
                                                            uptable["filterElementUsePercentage"])
                                                            streams["ice_maker_times_high"] = int2String(uptable
                                                            ["iceMakerTimesHigh"])
                                                            streams["ice_maker_times_low"] = int2String(uptable
                                                            ["iceMakerTimesLow"])
                                                            if (bodyLength >= 67) then
                                                                streams["lighting_effect"] = int2String(uptable
                                                                ["lightingEffect"])
                                                                streams["lighting_color"] = int2String(uptable
                                                                ["lightingColor"])
                                                                streams["custom_color_R"] = int2String(uptable
                                                                ["customColorR"])
                                                                streams["custom_color_G"] = int2String(uptable
                                                                ["customColorG"])
                                                                streams["custom_color_B"] = int2String(uptable
                                                                ["customColorB"])
                                                                if (uptable["turnOffLight"] == 0x01) then streams["turn_off_light"] =
                                                                    "off" elseif (uptable["turnOffLight"] == 0x00) then streams["turn_off_light"] =
                                                                    "on" end
                                                                if (uptable["lightBrightness"] == 0x02) then streams["light_brightness"] =
                                                                    "low" elseif (uptable["lightBrightness"] == 0x00) then streams["light_brightness"] =
                                                                    "high" end
                                                                if (uptable["sunnyForSevenDays"] == 0x00) then streams["sunny_for_seven_days"] =
                                                                    "off" elseif (uptable["sunnyForSevenDays"] == 0x04) then streams["sunny_for_seven_days"] =
                                                                    "on" end
                                                                if (uptable["standbyMode"] == 0x00) then streams["standby_mode"] =
                                                                    "off" elseif (uptable["standbyMode"] == 0x08) then streams["standby_mode"] =
                                                                    "on" end
                                                                if (uptable["quickFreezing"] == 0x00) then streams["quick_freezing"] =
                                                                    "off" elseif (uptable["quickFreezing"] == 0x10) then streams["quick_freezing"] =
                                                                    "on" end
                                                                streams["freezing_light_open"] = int2String(uptable
                                                                ["freezingLightOpen"])
                                                                if (uptable["freezingLightOpenChose"] == 0x00) then streams["freezing_light_open_chose"] =
                                                                    "off" elseif (uptable["freezingLightOpenChose"] == 0x20) then streams["freezing_light_open_chose"] =
                                                                    "on" end
                                                                if (bodyLength >= 72) then
                                                                    streams["wifi_human_induction_value"] = int2String(
                                                                    uptable["wifiHumanInductionValue"])
                                                                    if (bodyLength >= 73) then
                                                                        if (uptable["teslaHandleSwitchMode"] == 0x01) then streams["tesla_handle_switch_mode"] =
                                                                            "on" elseif (uptable["teslaHandleSwitchMode"] == 0x00) then streams["tesla_handle_switch_mode"] =
                                                                            "off" end
                                                                        if (uptable["fivePreservationMode"] == 0x02) then streams["five_preservation_mode"] =
                                                                            "on" elseif (uptable["fivePreservationMode"] == 0x00) then streams["five_preservation_mode"] =
                                                                            "off" end
                                                                        if (uptable["controlSugarFlag"] == 0x04) then streams["control_sugar_flag"] =
                                                                            "on" elseif (uptable["controlSugarFlag"] == 0x00) then streams["control_sugar_flag"] =
                                                                            "off" end
                                                                        if (uptable["strongControlSugarFlag"] == 0x08) then streams["strong_control_sugar_flag"] =
                                                                            "on" elseif (uptable["strongControlSugarFlag"] == 0x00) then streams["strong_control_sugar_flag"] =
                                                                            "off" end
                                                                        if (uptable["nightLightSwitch"] == 0x10) then streams["night_light_switch"] =
                                                                            "on" elseif (uptable["nightLightSwitch"] == 0x00) then streams["night_light_switch"] =
                                                                            "off" end
                                                                        if (uptable["openDoorTipsSwitch"] == 0x20) then streams["open_door_tips_switch"] =
                                                                            "on" elseif (uptable["openDoorTipsSwitch"] == 0x00) then streams["open_door_tips_switch"] =
                                                                            "off" end
                                                                        if (uptable["pulseSwitch"] == 0x40) then streams["pulse_switch"] =
                                                                            "on" elseif (uptable["pulseSwitch"] == 0x00) then streams["pulse_switch"] =
                                                                            "off" end
                                                                        if (uptable["deliveryMode"] == 0x80) then streams["delivery_mode"] =
                                                                            "on" elseif (uptable["deliveryMode"] == 0x00) then streams["delivery_mode"] =
                                                                            "off" end
                                                                        if (bodyLength >= 74) then
                                                                            streams["sabbath_exit_time"] = int2String(
                                                                            uptable["sabbathExitTime"])
                                                                            if (uptable["sabbathMode"] == 0x40) then streams["sabbath_mode"] =
                                                                                "on" elseif (uptable["sabbathMode"] == 0x80) then streams["sabbath_mode"] =
                                                                                "off" elseif (uptable["sabbathMode"] == 0x00) then streams["sabbath_mode"] =
                                                                                "hold" end
                                                                            if (bodyLength >= 75) then
                                                                                streams["control_sugar_time_low"] =
                                                                                int2String(uptable
                                                                                ["controlSugarTimeLow"])
                                                                                streams["control_sugar_time_high"] =
                                                                                int2String(uptable
                                                                                ["controlSugarTimeHigh"])
                                                                                if (bodyLength >= 77) then
                                                                                    streams["handle_return_time"] =
                                                                                    int2String(uptable
                                                                                    ["handleReturnTime"])
                                                                                    if (bodyLength >= 78) then
                                                                                        if (uptable["delayDefrostSwitch"] == 0x01) then streams["delay_defrost_switch"] =
                                                                                            "on" elseif (uptable["delayDefrostSwitch"] == 0x00) then streams["delay_defrost_switch"] =
                                                                                            "off" end
                                                                                        if (uptable["demandResponseSwitch"] == 0x02) then streams["demand_response_switch"] =
                                                                                            "on" elseif (uptable["demandResponseSwitch"] == 0x00) then streams["demand_response_switch"] =
                                                                                            "off" end
                                                                                        if (uptable["temporaryDeloadingSwitch"] == 0x04) then streams["temporary_deloading_switch"] =
                                                                                            "on" elseif (uptable["temporaryDeloadingSwitch"] == 0x00) then streams["temporary_deloading_switch"] =
                                                                                            "off" end
                                                                                        if (uptable["iceClean"] == 0x08) then streams["ice_clean"] =
                                                                                            "on" elseif (uptable["iceClean"] == 0x00) then streams["ice_clean"] =
                                                                                            "off" end
                                                                                        streams["deloading_maximum_exit_time"] =
                                                                                        int2String(uptable
                                                                                        ["deloadingMaximumExitTime"] * 2)
                                                                                    end
                                                                                    if (bodyLength >= 79) then
                                                                                        streams["defrost_maximum_exit_time"] =
                                                                                        int2String(uptable
                                                                                        ["defrostMaximumExitTime"]) * 0.5
                                                                                        streams["demand_response_maximum_exit_time"] =
                                                                                        int2String(uptable
                                                                                        ["demandResponseMaximumExitTime"]) *
                                                                                        0.5
                                                                                    end
                                                                                    if (bodyLength >= 80) then
                                                                                        if (uptable["telstarSavingMode"] == 0x01) then streams["telstar_saving_mode"] =
                                                                                            "on" elseif (uptable["telstarSavingMode"] == 0x00) then streams["telstar_saving_mode"] =
                                                                                            "off" end
                                                                                        if (uptable["panelDisplayGear"] == 0x02) then streams["panel_display_gear"] =
                                                                                            "on" elseif (uptable["panelDisplayGear"] == 0x00) then streams["panel_display_gear"] =
                                                                                            "off" end
                                                                                        if (uptable["offPeakDefrostSwitch"] == 0x08) then streams["off_peak_defrost_switch"] =
                                                                                            "on" elseif (uptable["offPeakDefrostSwitch"] == 0x00) then streams["off_peak_defrost_switch"] =
                                                                                            "off" end
                                                                                        streams["cooling_time_start_hour"] =
                                                                                        tostring((uptable["coolThresholdUpwardValue"] + 1) /
                                                                                        2)
                                                                                        streams["freeze_threshold_upward_value"] =
                                                                                        tostring((uptable["freezeThresholdUpwardValue"] + 1) /
                                                                                        2)
                                                                                        if (bodyLength >= 84) then
                                                                                            streams["cooling_time_start_hour"] =
                                                                                            int2String(uptable
                                                                                            ["coolingTimeStartHour"])
                                                                                            streams["cooling_time_start_minutes"] =
                                                                                            int2String(uptable
                                                                                            ["coolingTimeStartMinutes"])
                                                                                            streams["rise_time_start_hour"] =
                                                                                            int2String(uptable
                                                                                            ["riseTimeStartHour"])
                                                                                            streams["rise_time_start_minutes"] =
                                                                                            int2String(uptable
                                                                                            ["riseTimeStartMinutes"])
                                                                                        end
                                                                                        if (bodyLength >= 85) then
                                                                                            streams["storage_left_door_auto_open_angle"] =
                                                                                            int2String(uptable
                                                                                            ["storageLeftDoorAutoOpenAngle"])
                                                                                            streams["storage_right_door_auto_open_angle"] =
                                                                                            int2String(uptable
                                                                                            ["storageRightDoorAutoOpenAngle"])
                                                                                        end
                                                                                        if (bodyLength >= 86) then
                                                                                            streams["global_flex_temperature"] =
                                                                                            int2String(-12 -
                                                                                            uptable["globalFlexTemperature"])
                                                                                            if (bodyLength >= 87) then
                                                                                                streams["storage_glass_door_light"] =
                                                                                                int2String(uptable
                                                                                                ["storageGlassDoorLight"])
                                                                                                if (uptable["storageLightOpenChose"] == 0x08) then streams["storage_light_open_chose"] =
                                                                                                    "on" elseif (uptable["storageLightOpenChose"] == 0x00) then streams["storage_light_open_chose"] =
                                                                                                    "off" end
                                                                                                streams["storage_glass_door_light_open"] =
                                                                                                int2String(uptable
                                                                                                ["storageGlassDoorLightOpen"])
                                                                                                if (uptable["vegetableFreezing"] == 0x40) then streams["vegetable_freezing"] =
                                                                                                    "on" elseif (uptable["vegetableFreezing"] == 0x00) then streams["vegetable_freezing"] =
                                                                                                    "off" end
                                                                                                if (uptable["vegetableFreezingDry"] == 0x80) then streams["vegetable_freezing_dry"] =
                                                                                                    "on" elseif (uptable["vegetableFreezingDry"] == 0x00) then streams["vegetable_freezing_dry"] =
                                                                                                    "off" end
                                                                                                if (bodyLength >= 88) then
                                                                                                    streams["ai_fruit_display_control"] =
                                                                                                    int2String(uptable
                                                                                                    ["aiFruitDisplayControl"])
                                                                                                    if (uptable["aiFruitFlag"] == 0x08) then streams["ai_fruit_flag"] =
                                                                                                        "on" elseif (uptable["aiFruitFlag"] == 0x00) then streams["ai_fruit_flag"] =
                                                                                                        "off" end
                                                                                                    streams["ai_purine_display_control"] =
                                                                                                    int2String(uptable
                                                                                                    ["aiPurineDisplayControl"])
                                                                                                    if (uptable["aiPurineFlag"] == 0x80) then streams["ai_purine_flag"] =
                                                                                                        "on" elseif (uptable["aiPurineFlag"] == 0x00) then streams["ai_purine_flag"] =
                                                                                                        "off" end
                                                                                                end
                                                                                                if (bodyLength >= 89) then
                                                                                                    streams["ai_fruit_box_gear"] =
                                                                                                    int2String(uptable
                                                                                                    ["aiFruitBoxGear"])
                                                                                                    if (uptable["smartAiToSelfSelect"] == 0x08) then streams["smart_ai_to_self_select"] =
                                                                                                        "yes" elseif (uptable["smartAiToSelfSelect"] == 0x00) then streams["smart_ai_to_self_select"] =
                                                                                                        "no" end
                                                                                                    if (uptable["aiPurine2ndEstimate"] == 0x10) then streams["ai_purine_2nd_estimate"] =
                                                                                                        "process" elseif (uptable["aiPurine2ndEstimate"] == 0x00) then streams["ai_purine_2nd_estimate"] =
                                                                                                        "finish" end
                                                                                                    if (uptable["surfaceLightModeSelect"] == 0x20) then streams["surface_light_mode_select"] =
                                                                                                        "manual" elseif (uptable["surfaceLightModeSelect"] == 0x00) then streams["surface_light_mode_select"] =
                                                                                                        "automatic" end
                                                                                                    if (uptable["atmosphereLampModeSelect"] == 0x40) then streams["atmosphere_lamp_mode_select"] =
                                                                                                        "manual" elseif (uptable["atmosphereLampModeSelect"] == 0x00) then streams["atmosphere_lamp_mode_select"] =
                                                                                                        "automatic" end
                                                                                                end
                                                                                                if (bodyLength >= 90) then
                                                                                                    if (uptable["storageDoorAutoOpen"] == 0x01) then streams["storage_door_auto_open"] =
                                                                                                        "full" elseif (uptable["storageDoorAutoOpen"] == 0x00) then streams["storage_door_auto_open"] =
                                                                                                        "single" end
                                                                                                    if (uptable["tapTap"] == 0x02) then streams["tap_tap"] =
                                                                                                        "on" elseif (uptable["tapTap"] == 0x00) then streams["tap_tap"] =
                                                                                                        "off" end
                                                                                                    streams["wine_type"] =
                                                                                                    int2String(uptable
                                                                                                    ["wineType"])
                                                                                                    if (uptable["offlineVoiceSwitch"] == 0x10) then streams["offline_voice_switch"] =
                                                                                                        "on" elseif (uptable["offlineVoiceSwitch"] == 0x00) then streams["offline_voice_switch"] =
                                                                                                        "off" end
                                                                                                    streams["offline_voice_sensitivity"] =
                                                                                                    int2String(uptable
                                                                                                    ["offlineVoiceSensitivity"])
                                                                                                    if (uptable["cameraSwitch"] == 0x80) then streams["camera_switch"] =
                                                                                                        "on" elseif (uptable["cameraSwitch"] == 0x00) then streams["camera_switch"] =
                                                                                                        "off" end
                                                                                                end
                                                                                                if (bodyLength >= 91) then
                                                                                                    streams["led_pwm_duty"] =
                                                                                                    int2String(uptable
                                                                                                    ["ledPwmDuty"])
                                                                                                    if (uptable["sleepMode"] == 0x80) then streams["sleep_mode"] =
                                                                                                        "on" elseif (uptable["sleepMode"] == 0x00) then streams["sleep_mode"] =
                                                                                                        "off" end
                                                                                                end
                                                                                                if (bodyLength >= 92) then
                                                                                                    streams["sleep_mode_start_hour"] =
                                                                                                    int2String(uptable
                                                                                                    ["sleepModeStartHour"])
                                                                                                    if (uptable["roomLedDimmingFlag"] == 0x20) then streams["room_led_dimming_flag"] =
                                                                                                        "on" elseif (uptable["roomLedDimmingFlag"] == 0x00) then streams["room_led_dimming_flag"] =
                                                                                                        "off" end
                                                                                                    if (uptable["iceMachineStopIceFlag"] == 0x40) then streams["ice_machine_stop_ice_flag"] =
                                                                                                        "on" elseif (uptable["iceMachineStopIceFlag"] == 0x00) then streams["ice_machine_stop_ice_flag"] =
                                                                                                        "off" end
                                                                                                    if (uptable["displayBoardMuteFlag"] == 0x80) then streams["display_board_mute_flag"] =
                                                                                                        "on" elseif (uptable["displayBoardMuteFlag"] == 0x00) then streams["display_board_mute_flag"] =
                                                                                                        "off" end
                                                                                                    if (uptable["electronicCleanSmartMode"] == 0x40) then streams["electronic_clean_smart_mode"] =
                                                                                                        "on" elseif (uptable["electronicCleanSmartMode"] == 0x00) then streams["electronic_clean_smart_mode"] =
                                                                                                        "off" else streams["electronic_clean_smart_mode"] =
                                                                                                        "off" end
                                                                                                    streams["sleep_mode_start_minute"] =
                                                                                                    int2String(uptable
                                                                                                    ["sleepModeStartMinute"])
                                                                                                    streams["sleep_mode_end_hour"] =
                                                                                                    int2String(uptable
                                                                                                    ["sleepModeEndHour"])
                                                                                                    streams["sleep_mode_end_minute"] =
                                                                                                    int2String(uptable
                                                                                                    ["sleepModeEndMinute"])
                                                                                                end
                                                                                                if (bodyLength >= 96) then
                                                                                                    if (uptable["iceWaterMode"] == 0x01) then streams["ice_water_mode"] =
                                                                                                        "on" elseif (uptable["iceWaterMode"] == 0x00) then streams["ice_water_mode"] =
                                                                                                        "off" end
                                                                                                    if (uptable["smartRecommend"] == 0x02) then streams["smart_recommend"] =
                                                                                                        "on" elseif (uptable["smartRecommend"] == 0x00) then streams["smart_recommend"] =
                                                                                                        "off" end
                                                                                                    if (uptable["autoFill"] == 0x04) then streams["auto_fill"] =
                                                                                                        "on" elseif (uptable["autoFill"] == 0x00) then streams["auto_fill"] =
                                                                                                        "off" end
                                                                                                    if (uptable["dividerSupportAutoFill"] == 0x80) then streams["divider_support_auto_fill"] =
                                                                                                        "yes" elseif (uptable["dividerSupportAutoFill"] == 0x00) then streams["divider_support_auto_fill"] =
                                                                                                        "no" end
                                                                                                    if (uptable["overflowSensor"] == 0x40) then streams["overflow_sensor"] =
                                                                                                        "on" elseif (uptable["overflowSensor"] == 0x00) then streams["overflow_sensor"] =
                                                                                                        "off" end
                                                                                                    if (uptable["iceWaterMixType"] == 0x00) then streams["ice_water_mix_type"] =
                                                                                                        "full" elseif (uptable["iceWaterMixType"] == 0x08) then streams["ice_water_mix_type"] =
                                                                                                        "smash" end
                                                                                                    streams["ice_water_mix_proportion"] =
                                                                                                    int2String(uptable
                                                                                                    ["iceWaterMixProportion"])
                                                                                                    if (uptable["iceWaterMixTypeMorning"] == 0x00) then streams["ice_water_mix_type_morning"] =
                                                                                                        "full" elseif (uptable["iceWaterMixTypeMorning"] == 0x10) then streams["ice_water_mix_type_morning"] =
                                                                                                        "smash" end
                                                                                                    streams["ice_water_mix_proportion_morning"] =
                                                                                                    int2String(uptable
                                                                                                    ["iceWaterMixProportionMorning"])
                                                                                                    if (uptable["isMorningMode"] == 0x80) then streams["is_morning_mode"] =
                                                                                                        "yes" elseif (uptable["isMorningMode"] == 0x00) then streams["is_morning_mode"] =
                                                                                                        "no" end
                                                                                                    streams["smart_morning_start_hour"] =
                                                                                                    int2String(uptable
                                                                                                    ["smartMorningStartHour"])
                                                                                                    streams["smart_noon_start_hour"] =
                                                                                                    int2String(uptable
                                                                                                    ["smartNoonStartHour"])
                                                                                                    if (uptable["iceWaterMixTypeNoon"] == 0x00) then streams["ice_water_mix_type_noon"] =
                                                                                                        "full" elseif (uptable["iceWaterMixTypeNoon"] == 0x10) then streams["ice_water_mix_type_noon"] =
                                                                                                        "smash" end
                                                                                                    streams["ice_water_mix_proportion_noon"] =
                                                                                                    int2String(uptable
                                                                                                    ["iceWaterMixProportionNoon"])
                                                                                                    if (uptable["isNoonMode"] == 0x80) then streams["is_noon_mode"] =
                                                                                                        "yes" elseif (uptable["isNoonMode"] == 0x00) then streams["is_noon_mode"] =
                                                                                                        "no" end
                                                                                                    streams["smart_night_start_hour"] =
                                                                                                    int2String(uptable
                                                                                                    ["smartNightStartHour"])
                                                                                                    if (uptable["iceWaterMixTypeNight"] == 0x00) then streams["ice_water_mix_type_night"] =
                                                                                                        "full" elseif (uptable["iceWaterMixTypeNight"] == 0x10) then streams["ice_water_mix_type_night"] =
                                                                                                        "smash" end
                                                                                                    streams["ice_water_mix_proportion_night"] =
                                                                                                    int2String(uptable
                                                                                                    ["iceWaterMixProportionNight"])
                                                                                                    if (uptable["isNightMode"] == 0x80) then streams["is_night_mode"] =
                                                                                                        "yes" elseif (uptable["isNightMode"] == 0x00) then streams["is_night_mode"] =
                                                                                                        "no" end
                                                                                                    streams["water_box_status"] =
                                                                                                    int2String(uptable
                                                                                                    ["waterBoxStatus"])
                                                                                                end
                                                                                                if (bodyLength >= 100) then streams["open_door_warning_time"] =
                                                                                                    int2String(uptable
                                                                                                    ["openDoorWarningTime"]) end
                                                                                                if (bodyLength >= 101) then streams["open_door_hover_time"] =
                                                                                                    int2String(uptable
                                                                                                    ["openDoorHoverTime"]) end
                                                                                                if (bodyLength >= 102) then
                                                                                                    if (uptable["gpsReportSwitch"] == 0x01) then streams["gps_report_switch"] =
                                                                                                        "on" elseif (uptable["gpsReportSwitch"] == 0x00) then streams["gps_report_switch"] =
                                                                                                        "off" end
                                                                                                    if (uptable["freezerLightOneMinuteFlag"] == 0x02) then streams["freezer_light_one_minute_flag"] =
                                                                                                        "on" elseif (uptable["freezerLightOneMinuteFlag"] == 0x00) then streams["freezer_light_one_minute_flag"] =
                                                                                                        "off" end
                                                                                                    if (uptable["smartFreezeMode"] == 0x04) then streams["smart_freeze_mode"] =
                                                                                                        "on" elseif (uptable["smartFreezeMode"] == 0x00) then streams["smart_freeze_mode"] =
                                                                                                        "off" end
                                                                                                    if (uptable["smartCoolMode"] == 0x08) then streams["smart_cool_mode"] =
                                                                                                        "on" elseif (uptable["smartCoolMode"] == 0x00) then streams["smart_cool_mode"] =
                                                                                                        "off" end
                                                                                                    if (uptable["multiFuncZoneStatus"] == 0x10) then streams["multi_func_zone_status"] =
                                                                                                        "off" elseif (uptable["multiFuncZoneStatus"] == 0x00) then streams["multi_func_zone_status"] =
                                                                                                        "on" end
                                                                                                end
                                                                                                if (bodyLength >= 103) then
                                                                                                    if (uptable["appSmartSelectionMode"] == 0x01) then streams["app_smart_selection_mode"] =
                                                                                                        "on" elseif (uptable["appSmartSelectionMode"] == 0x00) then streams["app_smart_selection_mode"] =
                                                                                                        "off" end
                                                                                                    if (uptable["smartSelectionGearChange"] == 0x02) then streams["smart_selection_gear_change"] =
                                                                                                        "yes" elseif (uptable["smartSelectionGearChange"] == 0x00) then streams["smart_selection_gear_change"] =
                                                                                                        "no" end
                                                                                                    if (uptable["fridgeConstantTempHumidity"] == 0x04) then streams["fridge_constant_temp_humidity"] =
                                                                                                        "on" elseif (uptable["fridgeConstantTempHumidity"] == 0x00) then streams["fridge_constant_temp_humidity"] =
                                                                                                        "off" end
                                                                                                end
                                                                                                if (bodyLength >= 104) then streams["smart_selection_set_temp"] =
                                                                                                    int2String(uptable
                                                                                                    ["smartSelectionSetTemp"] -
                                                                                                    50) end
                                                                                                if (bodyLength >= 105) then streams["tmf_cool_freeze_mode"] =
                                                                                                    int2String(uptable
                                                                                                    ["tmfCoolFreezeMode"]) end
                                                                                                if (bodyLength >= 106) then
                                                                                                    streams["handle_atmosphere_lamp_brightness"] =
                                                                                                    int2String(uptable
                                                                                                    ["handleAtmosphereLampBrightness"])
                                                                                                    streams["colmo_cool_freeze_mode"] =
                                                                                                    int2String(uptable
                                                                                                    ["colmoCoolFreezeMode"])
                                                                                                end
                                                                                                if (bodyLength >= 110) then
                                                                                                    if (uptable["defrostModeSwitch"] == 0x01) then streams["defrost_mode_switch"] =
                                                                                                        "on" elseif (uptable["defrostModeSwitch"] == 0x00) then streams["defrost_mode_switch"] =
                                                                                                        "off" end
                                                                                                    if (uptable["defrostCompletedState"] == 0x02) then streams["defrost_completed_state"] =
                                                                                                        "yes" else streams["defrost_completed_state"] =
                                                                                                        "no" end
                                                                                                    if (bodyLength >= 111) then
                                                                                                        uptable["defrostRemainTime"] =
                                                                                                        uptable["defrostRemainTimeData111"] *
                                                                                                        64 +
                                                                                                        uptable["defrostRemainTimeData110"]
                                                                                                        streams["defrost_remain_time"] =
                                                                                                        int2String(
                                                                                                        uptable["defrostRemainTime"])
                                                                                                    end
                                                                                                    if (bodyLength >= 112) then streams["defrost_time_user_defined"] =
                                                                                                        int2String(
                                                                                                        uptable["defrostTimeUserDefined"]) end
                                                                                                end
                                                                                                if (bodyLength >= 113) then
                                                                                                    if (uptable["nfcSignalBoardEnabled"] == 0x01) then streams["nfc_signal_board_enabled"] =
                                                                                                        "on" elseif (uptable["nfcSignalBoardEnabled"] == 0x00) then streams["nfc_signal_board_enabled"] =
                                                                                                        "off" end
                                                                                                    if (uptable["nfcSignalBoardState"] == 0x08) then streams["nfc_signal_board_state"] =
                                                                                                        "on" elseif (uptable["nfcSignalBoardState"] == 0x00) then streams["nfc_signal_board_state"] =
                                                                                                        "off" end
                                                                                                end
                                                                                                if (bodyLength >= 117) then
                                                                                                    streams["food_clip_data116"] =
                                                                                                    uptable["foodClipData116"]
                                                                                                    streams["food_clip_data117"] =
                                                                                                    uptable["foodClipData117"]
                                                                                                end
                                                                                                if (bodyLength >= 118) then streams["wifi_human_induction_far_value"] =
                                                                                                    uptable["wifiHumanInductionFarValue"] end
                                                                                                if (bodyLength >= 119) then streams["wifi_human_induction_exist_value"] =
                                                                                                    uptable["wifiHumanInductionExistValue"] end
                                                                                                if (bodyLength >= 120) then streams["range_tracking_short_value"] =
                                                                                                    uptable["rangeTrackingShortValue"] end
                                                                                                if (bodyLength >= 121) then streams["range_tracking_far_value"] =
                                                                                                    uptable["rangeTrackingFarValue"] end
                                                                                                if (bodyLength >= 122) then streams["resist_spectrum_symmetry_disturb_ratio"] =
                                                                                                    uptable["resistSpectrumSymmetryDisturbRatio"] end
                                                                                                if (bodyLength >= 123) then streams["resist_spectrum_symmetry_disturb_num"] =
                                                                                                    uptable["resistSpectrumSymmetryDisturbNum"] end
                                                                                                if (bodyLength >= 124) then streams["ai_human_induction_similarity_value"] =
                                                                                                    uptable["aiHumanInductionSimilarityValue"] end
                                                                                                if (bodyLength >= 131) then
                                                                                                    if (uptable["basicPowerSavingSwitch"] == 0x01) then streams["basic_power_saving_switch"] =
                                                                                                        "on" elseif (uptable["basicPowerSavingSwitch"] == 0x00) then streams["basic_power_saving_switch"] =
                                                                                                        "off" end
                                                                                                    if (uptable["powerSavingStarVersion"] == 0x02) then streams["power_saving_star_version"] =
                                                                                                        "new" elseif (uptable["powerSavingStarVersion"] == 0x00) then streams["power_saving_star_version"] =
                                                                                                        "old" end
                                                                                                end
                                                                                                if (bodyLength >= 132) then streams["internal_deloading_maximum_exit_time"] =
                                                                                                    int2String(uptable
                                                                                                    ["internalDeloadingMaximumExitTime"] *
                                                                                                    2) end
                                                                                                if (bodyLength >= 133) then streams["smart_denoise_open_hours"] =
                                                                                                    int2String(uptable
                                                                                                    ["smartDenoiseOpenHours"]) end
                                                                                                if (bodyLength >= 134) then streams["smart_denoise_open_mins"] =
                                                                                                    int2String(uptable
                                                                                                    ["smartDenoiseOpenMins"]) end
                                                                                                if (bodyLength >= 135) then
                                                                                                    if (uptable["freezerElecPowerfulDeodorizeSwitch"] == 0x01) then streams["freezer_elec_powerful_deodorize_switch"] =
                                                                                                        "on" elseif (uptable["freezerElecPowerfulDeodorizeSwitch"] == 0x00) then streams["freezer_elec_powerful_deodorize_switch"] =
                                                                                                        "off" end
                                                                                                    streams["freezer_elec_powerful_deodorize_hour_time"] =
                                                                                                    int2String(uptable
                                                                                                    ["freezerElecPowerfulDeodorizeHourTime"])
                                                                                                end
                                                                                                if (bodyLength >= 136) then streams["freezer_elec_powerful_deodorize_min_time"] =
                                                                                                    int2String(uptable
                                                                                                    ["freezerElecPowerfulDeodorizeMinTime"]) end
                                                                                                if (bodyLength >= 137) then streams["storage_elec_powerful_deodorize_hour_time"] =
                                                                                                    int2String(uptable
                                                                                                    ["storageElecPowerfulDeodorizeHourTime"]) end
                                                                                            end
                                                                                        end
                                                                                    end
                                                                                end
                                                                            end
                                                                        end
                                                                    end
                                                                end
                                                            end
                                                        end
                                                    end
                                                end
                                            end
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end
    elseif ((uptable["dataType"] == 0x04 and bodyBytes[0] == 0x01) or (uptable["dataType"] == 0x03 and bodyBytes[0] == 0x01)) then
        if (uptable["codeMode"] == 0x01) then streams["storage_mode"] = "on" elseif (uptable["codeMode"] == 0x00) then streams["storage_mode"] =
            "off" end
        if (uptable["freezingMode"] == 0x02) then streams["freezing_mode"] = "on" elseif (uptable["freezingMode"] == 0x00) then streams["freezing_mode"] =
            "off" end
        if (uptable["smartMode"] == 0x04) then streams["intelligent_mode"] = "on" elseif (uptable["smartMode"] == 0x00) then streams["intelligent_mode"] =
            "off" end
        if (uptable["energySavingMode"] == 0x08) then streams["energy_saving_mode"] = "on" elseif (uptable["energySavingMode"] == 0x00) then streams["energy_saving_mode"] =
            "off" end
        if (uptable["holidayMode"] == 0x10) then streams["holiday_mode"] = "on" elseif (uptable["holidayMode"] == 0x00) then streams["holiday_mode"] =
            "off" end
        if (uptable["moisturizeMode"] == 0x20) then streams["moisturize_mode"] = "on" elseif (uptable["moisturizeMode"] == 0x00) then streams["moisturize_mode"] =
            "off" end
        if (uptable["preservationMode"] == 0x40) then streams["preservation_mode"] = "on" elseif (uptable["preservationMode"] == 0x00) then streams["preservation_mode"] =
            "off" end
        if (uptable["acmeFreezingMode"] == 0x80) then streams["acme_freezing_mode"] = "on" elseif (uptable["acmeFreezingMode"] == 0x00) then streams["acme_freezing_mode"] =
            "off" end
        if (uptable["radarMode"] == 0x01) then streams["radar_mode_power"] = "on" elseif (uptable["radarMode"] == 0x00) then streams["radar_mode_power"] =
            "off" end
        if (uptable["milkMode"] == 0x02) then streams["milk_mode_power"] = "on" elseif (uptable["milkMode"] == 0x00) then streams["milk_mode_power"] =
            "off" end
        if (uptable["icedMode"] == 0x04) then streams["icea_mode_power"] = "on" elseif (uptable["icedMode"] == 0x00) then streams["icea_mode_power"] =
            "off" end
        if (uptable["plasmaAsepticMode"] == 0x08) then streams["plasma_aseptic_mode_power"] = "on" elseif (uptable["plasmaAsepticMode"] == 0x00) then streams["plasma_aseptic_mode_power"] =
            "off" end
        if (uptable["freezingIceMachinePower"] == 0x80) then streams["freezing_ice_machine_power"] = "on" elseif (uptable["freezingIceMachinePower"] == 0x00) then streams["freezing_ice_machine_power"] =
            "off" end
        if (uptable["removeDew"] == 0x01) then streams["remove_dew_power"] = "on" elseif (uptable["removeDew"] == 0x00) then streams["remove_dew_power"] =
            "off" end
        if (uptable["humidify"] == 0x02) then streams["humidify_power"] = "on" elseif (uptable["humidify"] == 0x00) then streams["humidify_power"] =
            "off" end
        if (uptable["unfreeze"] == 0x04) then streams["unfreeze_power"] = "on" elseif (uptable["unfreeze"] == 0x00) then streams["unfreeze_power"] =
            "off" end
        if (uptable["temperatureUnit"] == 0x08) then streams["temperature_unit"] = "fahrenheit" elseif (uptable["temperatureUnit"] == 0x00) then streams["temperature_unit"] =
            "celsius" end
        if (uptable["floodlight"] == 0x10) then streams["floodlight_power"] = "on" elseif (uptable["floodlight"] == 0x00) then streams["floodlight_power"] =
            "off" end
        if (uptable["functionSwitch"] == 0x00) then streams["icea_bar_function_switch"] = "default" elseif (uptable["functionSwitch"] == 0x40) then streams["icea_bar_function_switch"] =
            "refrigeration" elseif (uptable["functionSwitch"] == 0x80) then streams["icea_bar_function_switch"] =
            "freezing" end
        if (uptable["refrigerationPowerValue"] == 0x00) then streams["storage_power"] = "on" elseif (uptable["refrigerationPowerValue"] == 0x01) then streams["storage_power"] =
            "off" end
        if (uptable["lVariablePowerValue"] == 0x00) then streams["left_flexzone_power"] = "on" elseif (uptable["lVariablePowerValue"] == 0x04) then streams["left_flexzone_power"] =
            "off" end
        if (uptable["rVariablePowerValue"] == 0x00) then streams["right_flexzone_power"] = "on" elseif (uptable["rVariablePowerValue"] == 0x08) then streams["right_flexzone_power"] =
            "off" end
        if (uptable["freezingPowerValue"] == 0x00) then streams["freezing_power"] = "on" elseif (uptable["freezingPowerValue"] == 0x10) then streams["freezing_power"] =
            "off" end
        if (uptable["crossPeakElectricity"] == 0x40) then streams["cross_peak_electricity"] = "on" elseif (uptable["crossPeakElectricity"] == 0x00) then streams["cross_peak_electricity"] =
            "off" end
        if (uptable["allRefrigerationPower"] == 0x80) then streams["all_refrigeration_power"] = "on" elseif (uptable["allRefrigerationPower"] == 0x00) then streams["all_refrigeration_power"] =
            "off" end
        streams["storage_temperature"] = int2String(uptable["refrigerationTemperature"])
        streams["freezing_temperature"] = int2String(-12 - uptable["freezingTemperature"])
        if ((uptable["lVariableTemperature"] >= 1) and (uptable["lVariableTemperature"] <= 29)) then streams["left_flexzone_temperature"] =
            int2String(uptable["lVariableTemperature"] - 19) elseif ((uptable["lVariableTemperature"] >= 49) and (uptable["lVariableTemperature"] <= 54)) then streams["left_flexzone_temperature"] =
            int2String(30 - uptable["lVariableTemperature"]) else streams["left_flexzone_temperature"] = "0" end
        if ((uptable["rVariableTemperature"] >= 1) and (uptable["rVariableTemperature"] <= 29)) then streams["right_flexzone_temperature"] =
            int2String(uptable["rVariableTemperature"] - 19) elseif ((uptable["rVariableTemperature"] >= 49) and (uptable["rVariableTemperature"] <= 54)) then streams["right_flexzone_temperature"] =
            int2String(30 - uptable["rVariableTemperature"]) else streams["right_flexzone_temperature"] = "0" end
        streams["interval_room_humidity_level"] = int2String(uptable["intervalRoomHumidityLevel"])
        if (uptable["variableModeValue"] == 0x01) then streams["variable_mode"] = "soft_freezing_mode" elseif (uptable["variableModeValue"] == 0x00) then streams["variable_mode"] =
            "none_mode" elseif (uptable["variableModeValue"] == 0x02) then streams["variable_mode"] = "zero_fresh_mode" elseif (uptable["variableModeValue"] == 0x03) then streams["variable_mode"] =
            "cold_drink_mode" elseif (uptable["variableModeValue"] == 0x04) then streams["variable_mode"] =
            "fresh_product_mode" elseif (uptable["variableModeValue"] == 0x05) then streams["variable_mode"] =
            "partial_freezing_mode" elseif (uptable["variableModeValue"] == 0x06) then streams["variable_mode"] =
            "dry_zone_mode" elseif (uptable["variableModeValue"] == 0x07) then streams["variable_mode"] =
            "freeze_warm_mode" elseif (uptable["variableModeValue"] == 0x08) then streams["variable_mode"] =
            "freeze_mode" end
        streams["freeze_fahrenheit_level"] = int2String(uptable["freezingFahrenheit"])
        streams["refrigeration_fahrenheit_level"] = int2String(uptable["refrigerationFahrenheit"])
        streams["normal_zone_level"] = int2String(uptable["normalTemperatureLevel"])
        streams["function_zone_level"] = int2String(uptable["functionZoneLevel"])
        if (uptable["microcrystalFresh"] == 0x01) then streams["microcrystal_fresh"] = "on" elseif (uptable["microcrystalFresh"] == 0x00) then streams["microcrystal_fresh"] =
            "off" end
        if (uptable["humidity"] == 0x10) then streams["humidity"] = "high" elseif (uptable["humidity"] == 0x20) then streams["humidity"] =
            "low" end
        if (uptable["performanceMode"] == 0x80) then streams["performance_mode"] = "on" elseif (uptable["performanceMode"] == 0x00) then streams["performance_mode"] =
            "off" end
        if (uptable["electronicCleanStrong"] == 0x01) then streams["electronic_clean_strong"] = "on" elseif (uptable["electronicCleanStrong"] == 0x00) then streams["electronic_clean_strong"] =
            "off" end
        streams["electronic_clean_timeout"] = int2String(uptable["electronicCleanTimeout"])
        streams["quick_beverage_time"] = int2String(uptable["quickBeverageTime"])
        if (uptable["quickBeverage"] == 0x80) then streams["quick_beverage"] = "on" elseif (uptable["quickBeverage"] == 0x00) then streams["quick_beverage"] =
            "off" end
        if (uptable["globalFlexTemperature"] ~= nil) then streams["global_flex_temperature"] = int2String(-12 -
            uptable["globalFlexTemperature"]) end
    elseif (uptable["dataType"] == 0x04 and bodyBytes[0] == 0x00) then
        if (uptable["refrigerationDoorPower"] == 0x01) then streams["storage_door_state"] = "on" elseif (uptable["refrigerationDoorPower"] == 0x00) then streams["storage_door_state"] =
            "off" end
        if (uptable["freezingDoorPower"] == 0x02) then streams["freezer_door_state"] = "on" elseif (uptable["freezingDoorPower"] == 0x00) then streams["freezer_door_state"] =
            "off" end
        if (uptable["barDoorPower"] == 0x04) then streams["bar_door_state"] = "on" elseif (uptable["barDoorPower"] == 0x00) then streams["bar_door_state"] =
            "off" end
        if (uptable["iceMouthPower"] == 0x08) then streams["ice_mouth_power"] = "on" elseif (uptable["iceMouthPower"] == 0x00) then streams["ice_mouth_power"] =
            "off" end
        if (uptable["variableDoorPower"] == 0x10) then streams["flexzone_door_state"] = "on" elseif (uptable["variableDoorPower"] == 0x00) then streams["flexzone_door_state"] =
            "off" end
        if (uptable["storageIceHomeDoorState"] == 0x10) then streams["storage_ice_home_door_state"] = "on" elseif (uptable["storageIceHomeDoorState"] == 0x00) then streams["storage_ice_home_door_state"] =
            "off" end
        if (uptable["purineInhibitDrawerSwitch"] == 0x20) then streams["purine_inhibit_drawer_switch"] = "on" elseif (uptable["purineInhibitDrawerSwitch"] == 0x00) then streams["purine_inhibit_drawer_switch"] =
            "off" end
        if (uptable["storageModeCompletion"] == 0x01) then streams["storage_mode_completion"] = "yes" elseif (uptable["storageModeCompletion"] == 0x00) then streams["storage_mode_completion"] =
            "no" end
        if (uptable["freezingModeCompletion"] == 0x02) then streams["freezing_mode_completion"] = "yes" elseif (uptable["freezingModeCompletion"] == 0x00) then streams["freezing_mode_completion"] =
            "no" end
        if (uptable["humidifierWaterShortage"] == 0x04) then streams["humidifier_water_shortage"] = "yes" elseif (uptable["humidifierWaterShortage"] == 0x00) then streams["humidifier_water_shortage"] =
            "no" end
        if (uptable["plasmaAsepticCompletion"] == 0x08) then streams["plasma_aseptic_completion"] = "yes" elseif (uptable["plasmaAsepticCompletion"] == 0x00) then streams["plasma_aseptic_completion"] =
            "no" end
        if (uptable["acmeFreezingCompletion"] == 0x10) then streams["acme_freezing_completion"] = "yes" elseif (uptable["acmeFreezingCompletion"] == 0x00) then streams["acme_freezing_completion"] =
            "no" end
        if (uptable["eradicatePesticideResidueCompletion"] == 0x20) then streams["eradicate_pesticide_residue_completion"] =
            "yes" elseif (uptable["eradicatePesticideResidueCompletion"] == 0x00) then streams["eradicate_pesticide_residue_completion"] =
            "no" end
        if (uptable["quickBeverageCompletion"] == 0x80) then streams["quick_beverage_completion"] = "yes" elseif (uptable["quickBeverageCompletion"] == 0x00) then streams["quick_beverage_completion"] =
            "no" end
    elseif (uptable["dataType"] == 0x04 and bodyBytes[0] == 0x04) then if #bodyBytes >= 6 then
            uptable["humanSensingTriggerState"] = bit.band(bodyBytes[5], 0x80)
            if (uptable["humanSensingTriggerState"] == 0x80) then streams["human_sensing_trigger_state"] = "yes" elseif (uptable["humanSensingTriggerState"] == 0x00) then streams["human_sensing_trigger_state"] =
                "no" end
        end elseif ((uptable["dataType"] == 0x06 and bodyBytes[0] == 0x01) or (uptable["dataType"] == 0x03 and bodyBytes[0] == 0x02)) then
        if (uptable["isError"] == 0x01) then streams["is_error"] = "yes" elseif (uptable["isError"] == 0x00) then streams["is_error"] =
            "no" end
        if (uptable["storageDoorOpenOvertime"] == 0x01) then streams["storage_door_open_overtime"] = "yes" elseif (uptable["storageDoorOpenOvertime"] == 0x00) then streams["storage_door_open_overtime"] =
            "no" end
        if (uptable["freezerDoorOpenOvertime"] == 0x02) then streams["freezer_door_open_overtime"] = "yes" elseif (uptable["freezerDoorOpenOvertime"] == 0x00) then streams["freezer_door_open_overtime"] =
            "no" end
        if (uptable["barDoorOpenOvertime"] == 0x04) then streams["bar_door_open_overtime"] = "yes" elseif (uptable["barDoorOpenOvertime"] == 0x00) then streams["bar_door_open_overtime"] =
            "no" end
        if (uptable["variableDoorOpenOvertime"] == 0x08) then streams["variable_door_open_overtime"] = "yes" elseif (uptable["variableDoorOpenOvertime"] == 0x00) then streams["variable_door_open_overtime"] =
            "no" end
        if (uptable["iceMachineFull"] == 0x10) then streams["ice_machine_full"] = "yes" elseif (uptable["iceMachineFull"] == 0x00) then streams["ice_machine_full"] =
            "no" end
        if (uptable["refrigerationSensorError"] == 0x01) then streams["refrigeration_sensor_error"] = "yes" elseif (uptable["refrigerationSensorError"] == 0x00) then streams["refrigeration_sensor_error"] =
            "no" end
        if (uptable["refrigerationDefrostingSensorError"] == 0x02) then streams["refrigeration_defrosting_sensor_error"] =
            "yes" elseif (uptable["refrigerationDefrostingSensorError"] == 0x00) then streams["refrigeration_defrosting_sensor_error"] =
            "no" end
        if (uptable["ringTemperatureSensorError"] == 0x04) then streams["ring_temperature_sensor_error"] = "yes" elseif (uptable["ringTemperatureSensorError"] == 0x00) then streams["ring_temperature_sensor_error"] =
            "no" end
        if (uptable["flexzoneSensorError"] == 0x08) then streams["flexzone_sensor_error"] = "yes" elseif (uptable["flexzoneSensorError"] == 0x00) then streams["flexzone_sensor_error"] =
            "no" end
        if (uptable["rightFlexzoneSensorError"] == 0x10) then streams["right_flexzone_sensor_error"] = "yes" elseif (uptable["rightFlexzoneSensorError"] == 0x00) then streams["right_flexzone_sensor_error"] =
            "no" end
        if (uptable["freezingHighTemperature"] == 0x20) then streams["freezing_high_temperature"] = "yes" elseif (uptable["freezingHighTemperature"] == 0x00) then streams["freezing_high_temperature"] =
            "no" end
        if (uptable["freezingSensorError"] == 0x40) then streams["freezing_sensor_error"] = "yes" elseif (uptable["freezingSensorError"] == 0x00) then streams["freezing_sensor_error"] =
            "no" end
        if (uptable["freezingDefrostingSensorError"] == 0x80) then streams["freezing_defrosting_sensor_error"] = "yes" elseif (uptable["freezingDefrostingSensorError"] == 0x00) then streams["freezing_defrosting_sensor_error"] =
            "no" end
        if (uptable["iceElectricalMachineryError"] == 0x01) then streams["ice_electrical_machinery_error"] = "yes" elseif (uptable["iceElectricalMachineryError"] == 0x00) then streams["ice_electrical_machinery_error"] =
            "no" end
        if (uptable["refrigerationDefrostingOvertime"] == 0x02) then streams["refrigeration_defrosting_overtime"] = "yes" elseif (uptable["refrigerationDefrostingOvertime"] == 0x00) then streams["refrigeration_defrosting_overtime"] =
            "no" end
        if (uptable["freezingDefrostingOvertime"] == 0x04) then streams["freezing_defrosting_overtime"] = "yes" elseif (uptable["freezingDefrostingOvertime"] == 0x00) then streams["freezing_defrosting_overtime"] =
            "no" end
        if (uptable["zeroCrossingCheckError"] == 0x08) then streams["zero_crossing_check_error"] = "yes" elseif (uptable["zeroCrossingCheckError"] == 0x00) then streams["zero_crossing_check_error"] =
            "no" end
        if (uptable["eepromReadWriteError"] == 0x10) then streams["eeprom_read_write_error"] = "yes" elseif (uptable["eepromReadWriteError"] == 0x00) then streams["eeprom_read_write_error"] =
            "no" end
        if (uptable["leftFlexzoneSensorError"] == 0x20) then streams["left_flexzone_sensor_error"] = "yes" elseif (uptable["leftFlexzoneSensorError"] == 0x00) then streams["left_flexzone_sensor_error"] =
            "no" end
        if (uptable["iceRoomSensorError"] == 0x40) then streams["ice_room_sensor_error"] = "yes" elseif (uptable["iceRoomSensorError"] == 0x00) then streams["ice_room_sensor_error"] =
            "no" end
        if (uptable["mainDisplayCorrespondError"] == 0x80) then streams["main_display_correspond_error"] = "yes" elseif (uptable["mainDisplayCorrespondError"] == 0x00) then streams["main_display_correspond_error"] =
            "no" end
        if (uptable["iceMachineTemperatureError"] == 0x01) then streams["ice_machine_temperature_error"] = "yes" elseif (uptable["iceMachineTemperatureError"] == 0x00) then streams["ice_machine_temperature_error"] =
            "no" end
        if (uptable["flexzoneDefrostingSensorError"] == 0x02) then streams["flexzone_defrosting_sensor_error"] = "yes" elseif (uptable["flexzoneDefrostingSensorError"] == 0x00) then streams["flexzone_defrosting_sensor_error"] =
            "no" end
        if (uptable["flexzoneDefrostingSensor2Error"] == 0x04) then streams["flexzone_defrosting_sensor2_error"] = "yes" elseif (uptable["flexzoneDefrostingSensor2Error"] == 0x00) then streams["flexzone_defrosting_sensor2_error"] =
            "no" end
        if (uptable["yogurtMachineSensorError"] == 0x08) then streams["yogurt_machine_sensor_error"] = "yes" elseif (uptable["yogurtMachineSensorError"] == 0x00) then streams["yogurt_machine_sensor_error"] =
            "no" end
        if (uptable["iceMachineFrettingSwitchError"] == 0x10) then streams["ice_machine_fretting_switch_error"] = "yes" elseif (uptable["iceMachineFrettingSwitchError"] == 0x00) then streams["ice_machine_fretting_switch_error"] =
            "no" end
        if (uptable["iceMachinePipeFilterOvertime"] == 0x20) then streams["ice_machine_pipe_filter_overtime"] = "yes" elseif (uptable["iceMachinePipeFilterOvertime"] == 0x00) then streams["ice_machine_pipe_filter_overtime"] =
            "no" end
        if (uptable["ambientHumiditySensorError"] == 0x40) then streams["ambient_humidity_sensor_error"] = "yes" elseif (uptable["ambientHumiditySensorError"] == 0x00) then streams["ambient_humidity_sensor_error"] =
            "no" end
        if (uptable["storageHumiditySensorError"] == 0x80) then streams["storage_humidity_sensor_error"] = "yes" elseif (uptable["storageHumiditySensorError"] == 0x00) then streams["storage_humidity_sensor_error"] =
            "no" end
        if (uptable["radarSensor1Error"] == 0x01) then streams["radar_sensor1_error"] = "yes" elseif (uptable["radarSensor1Error"] == 0x00) then streams["radar_sensor1_error"] =
            "no" end
        if (uptable["radarSensor2Error"] == 0x02) then streams["radar_sensor2_error"] = "yes" elseif (uptable["radarSensor2Error"] == 0x00) then streams["radar_sensor2_error"] =
            "no" end
        if (uptable["radarSensor3Error"] == 0x04) then streams["radar_sensor3_error"] = "yes" elseif (uptable["radarSensor3Error"] == 0x00) then streams["radar_sensor3_error"] =
            "no" end
        if (uptable["radarSensor4Error"] == 0x08) then streams["radar_sensor4_error"] = "yes" elseif (uptable["radarSensor4Error"] == 0x00) then streams["radar_sensor4_error"] =
            "no" end
        if (uptable["radarSensor5Error"] == 0x10) then streams["radar_sensor5_error"] = "yes" elseif (uptable["radarSensor5Error"] == 0x00) then streams["radar_sensor5_error"] =
            "no" end
        if (uptable["functionZoneTemperatureSensorError"] == 0x20) then streams["function_zone_temperature_sensor_error"] =
            "yes" elseif (uptable["functionZoneTemperatureSensorError"] == 0x00) then streams["function_zone_temperature_sensor_error"] =
            "no" end
        if (uptable["normalZoneTemperatureSensorError"] == 0x40) then streams["normal_zone_temperature_sensor_error"] =
            "yes" elseif (uptable["normalZoneTemperatureSensorError"] == 0x00) then streams["normal_zone_temperature_sensor_error"] =
            "no" end
        if (uptable["humidityControlSensorError"] == 0x80) then streams["humidity_control_sensor_error"] = "yes" elseif (uptable["humidityControlSensorError"] == 0x00) then streams["humidity_control_sensor_error"] =
            "no" end
        if (uptable["openDoorTooFrequently"] == 0x01) then streams["open_door_too_frequently"] = "yes" elseif (uptable["openDoorTooFrequently"] == 0x00) then streams["open_door_too_frequently"] =
            "no" end
        if (uptable["storageDoorAloneOpenFrequently"] == 0x02) then streams["storage_door_alone_open_frequently"] = "yes" elseif (uptable["storageDoorAloneOpenFrequently"] == 0x00) then streams["storage_door_alone_open_frequently"] =
            "no" end
        if (uptable["freezingDoorAloneOpenFrequently"] == 0x04) then streams["freezing_door_alone_open_frequently"] =
            "yes" elseif (uptable["freezingDoorAloneOpenFrequently"] == 0x00) then streams["freezing_door_alone_open_frequently"] =
            "no" end
        if (uptable["barDoorAloneOpenFrequently"] == 0x08) then streams["bar_door_alone_open_frequently"] = "yes" elseif (uptable["barDoorAloneOpenFrequently"] == 0x00) then streams["bar_door_alone_open_frequently"] =
            "no" end
        if (uptable["snWritingError"] == 0x20) then streams["sn_writing_error"] = "yes" elseif (uptable["snWritingError"] == 0x00) then streams["sn_writing_error"] =
            "no" end
        if (uptable["storageTemperatureOverheating"] == 0x40) then streams["storage_temperature_overheating"] = "yes" elseif (uptable["storageTemperatureOverheating"] == 0x00) then streams["storage_temperature_overheating"] =
            "no" end
        if (uptable["storageTemperatureTooLow"] == 0x80) then streams["storage_temperature_too_low"] = "yes" elseif (uptable["storageTemperatureTooLow"] == 0x00) then streams["storage_temperature_too_low"] =
            "no" end
        if (uptable["storageHeatingWireSensorError"] == 0x01) then streams["storage_heating_wire_sensor_error"] = "yes" elseif (uptable["storageHeatingWireSensorError"] == 0x00) then streams["storage_heating_wire_sensor_error"] =
            "no" end
        if (uptable["uartReceiverError"] == 0x02) then streams["uart_receiver_error"] = "yes" elseif (uptable["uartReceiverError"] == 0x00) then streams["uart_receiver_error"] =
            "no" end
        if (uptable["crystalliteMainSensorError"] == 0x08) then streams["crystallite_main_sensor_error"] = "yes" elseif (uptable["crystalliteMainSensorError"] == 0x00) then streams["crystallite_main_sensor_error"] =
            "no" end
        if (uptable["crystalliteBase1SensorError"] == 0x10) then streams["crystallite_base1_sensor_error"] = "yes" elseif (uptable["crystalliteBase1SensorError"] == 0x00) then streams["crystallite_base1_sensor_error"] =
            "no" end
        if (uptable["crystalliteBase2SensorError"] == 0x20) then streams["crystallite_base2_sensor_error"] = "yes" elseif (uptable["crystalliteBase2SensorError"] == 0x00) then streams["crystallite_base2_sensor_error"] =
            "no" end
        if (uptable["crystalliteBase3SensorError"] == 0x40) then streams["crystallite_base3_sensor_error"] = "yes" elseif (uptable["crystalliteBase3SensorError"] == 0x00) then streams["crystallite_base3_sensor_error"] =
            "no" end
        if (uptable["crystalliteBase4SensorError"] == 0x80) then streams["crystallite_base4_sensor_error"] = "yes" elseif (uptable["crystalliteBase4SensorError"] == 0x00) then streams["crystallite_base4_sensor_error"] =
            "no" end
        if (uptable["iceRoomDoorOpenOvertime"] == 0x01) then streams["ice_room_door_open_overtime"] = "yes" elseif (uptable["iceRoomDoorOpenOvertime"] == 0x00) then streams["ice_room_door_open_overtime"] =
            "no" end
        if (uptable["storageIceFullTips"] == 0x02) then streams["storage_ice_full_tips"] = "yes" elseif (uptable["storageIceFullTips"] == 0x00) then streams["storage_ice_full_tips"] =
            "no" end
        if (uptable["iceMachineSensorError"] == 0x04) then streams["ice_machine_sensor_error"] = "yes" elseif (uptable["iceMachineSensorError"] == 0x00) then streams["ice_machine_sensor_error"] =
            "no" end
        if (uptable["storageIceMachineSensorError"] == 0x08) then streams["storage_ice_machine_sensor_error"] = "yes" elseif (uptable["storageIceMachineSensorError"] == 0x00) then streams["storage_ice_machine_sensor_error"] =
            "no" end
        if (uptable["storageIceOperationError"] == 0x10) then streams["storage_ice_operation_error"] = "yes" elseif (uptable["storageIceOperationError"] == 0x00) then streams["storage_ice_operation_error"] =
            "no" end
        if (uptable["freezingIceOperationError"] == 0x20) then streams["freezing_ice_operation_error"] = "yes" elseif (uptable["freezingIceOperationError"] == 0x00) then streams["freezing_ice_operation_error"] =
            "no" end
        if (uptable["mcuIceCommunicationError"] == 0x40) then streams["mcu_ice_communication_error"] = "yes" elseif (uptable["mcuIceCommunicationError"] == 0x00) then streams["mcu_ice_communication_error"] =
            "no" end
        if (uptable["mcuFiveCommunicationError"] == 0x01) then streams["mcu_five_communication_error"] = "yes" elseif (uptable["mcuFiveCommunicationError"] == 0x00) then streams["mcu_five_communication_error"] =
            "no" end
        if (uptable["fiveTslCommunicationError"] == 0x02) then streams["five_tsl_communication_error"] = "yes" elseif (uptable["fiveTslCommunicationError"] == 0x00) then streams["five_tsl_communication_error"] =
            "no" end
        if (uptable["twoTslCommunicationError"] == 0x04) then streams["two_tsl_communication_error"] = "yes" elseif (uptable["twoTslCommunicationError"] == 0x00) then streams["two_tsl_communication_error"] =
            "no" end
        if (uptable["fiveNOError"] == 0x08) then streams["five_N_O_error"] = "yes" elseif (uptable["fiveNOError"] == 0x00) then streams["five_N_O_error"] =
            "no" end
        if (uptable["fiveCTError"] == 0x10) then streams["five_ct_error"] = "yes" elseif (uptable["fiveCTError"] == 0x00) then streams["five_ct_error"] =
            "no" end
        if (uptable["freezerWaterShortageAlarm"] == 0x20) then streams["freezer_water_shortage_alarm"] = "yes" elseif (uptable["freezerWaterShortageAlarm"] == 0x00) then streams["freezer_water_shortage_alarm"] =
            "no" end
    end
    local retTable = {}
    retTable["status"] = streams
    local ret = encode(retTable)
    return ret
end
