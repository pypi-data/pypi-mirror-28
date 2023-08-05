

class CANifier {

  void * m_handle;

public:
  void create1(int deviceNumber) {
    m_handle = c_CANifier_Create1(deviceNumber);
  }

  ctre::phoenix::ErrorCode setLEDOutput(uint32_t dutyCycle, uint32_t ledChannel) {
    
    auto __ret =  c_CANifier_SetLEDOutput(m_handle, dutyCycle, ledChannel );
    return __ret;
  }


  ctre::phoenix::ErrorCode setGeneralOutputs(uint32_t outputsBits, uint32_t isOutputBits) {
    
    auto __ret =  c_CANifier_SetGeneralOutputs(m_handle, outputsBits, isOutputBits );
    return __ret;
  }


  ctre::phoenix::ErrorCode setGeneralOutput(uint32_t outputPin, bool outputValue, bool outputEnable) {
    
    auto __ret =  c_CANifier_SetGeneralOutput(m_handle, outputPin, outputValue, outputEnable );
    return __ret;
  }


  ctre::phoenix::ErrorCode setPWMOutput(uint32_t pwmChannel, uint32_t dutyCycle) {
    
    auto __ret =  c_CANifier_SetPWMOutput(m_handle, pwmChannel, dutyCycle );
    return __ret;
  }


  ctre::phoenix::ErrorCode enablePWMOutput(uint32_t pwmChannel, bool bEnable) {
    
    auto __ret =  c_CANifier_EnablePWMOutput(m_handle, pwmChannel, bEnable );
    return __ret;
  }


  std::tuple<ctre::phoenix::ErrorCode, bool> getGeneralInput(uint32_t inputPin) {
    bool measuredInput;
    auto __ret =  c_CANifier_GetGeneralInput(m_handle, inputPin, &measuredInput );
    return std::make_tuple(__ret, measuredInput);
  }


  std::tuple<ctre::phoenix::ErrorCode, std::array<double, 2>> getPWMInput(uint32_t pwmChannel) {
    std::array<double, 2> dutyCycleAndPeriod;
    auto __ret =  c_CANifier_GetPWMInput(m_handle, pwmChannel, dutyCycleAndPeriod.data() );
    return std::make_tuple(__ret, dutyCycleAndPeriod);
  }


  ctre::phoenix::ErrorCode getLastError() {
    
    auto __ret =  c_CANifier_GetLastError(m_handle );
    return __ret;
  }


  std::tuple<ctre::phoenix::ErrorCode, double> getBusVoltage() {
    double batteryVoltage;
    auto __ret =  c_CANifier_GetBusVoltage(m_handle, &batteryVoltage );
    return std::make_tuple(__ret, batteryVoltage);
  }


  void setLastError(int error) {
    
     c_CANifier_SetLastError(m_handle, error );
    
  }


  ctre::phoenix::ErrorCode configSetParameter(int param, double value, int subValue, int ordinal, int timeoutMs) {
    
    auto __ret =  c_CANifier_ConfigSetParameter(m_handle, param, value, subValue, ordinal, timeoutMs );
    return __ret;
  }


  std::tuple<ctre::phoenix::ErrorCode, double> configGetParameter(int param, int ordinal, int timeoutMs) {
    double value;
    auto __ret =  c_CANifier_ConfigGetParameter(m_handle, param, &value, ordinal, timeoutMs );
    return std::make_tuple(__ret, value);
  }


  ctre::phoenix::ErrorCode configSetCustomParam(int newValue, int paramIndex, int timeoutMs) {
    
    auto __ret =  c_CANifier_ConfigSetCustomParam(m_handle, newValue, paramIndex, timeoutMs );
    return __ret;
  }


  std::tuple<ctre::phoenix::ErrorCode, int> configGetCustomParam(int paramIndex, int timoutMs) {
    int readValue;
    auto __ret =  c_CANifier_ConfigGetCustomParam(m_handle, &readValue, paramIndex, timoutMs );
    return std::make_tuple(__ret, readValue);
  }


  std::tuple<ctre::phoenix::ErrorCode, int> getFaults() {
    int param;
    auto __ret =  c_CANifier_GetFaults(m_handle, &param );
    return std::make_tuple(__ret, param);
  }


  std::tuple<ctre::phoenix::ErrorCode, int> getStickyFaults() {
    int param;
    auto __ret =  c_CANifier_GetStickyFaults(m_handle, &param );
    return std::make_tuple(__ret, param);
  }


  ctre::phoenix::ErrorCode clearStickyFaults(int timeoutMs) {
    
    auto __ret =  c_CANifier_ClearStickyFaults(m_handle, timeoutMs );
    return __ret;
  }


  std::tuple<ctre::phoenix::ErrorCode, int> getFirmwareVersion() {
    int firmwareVers;
    auto __ret =  c_CANifier_GetFirmwareVersion(m_handle, &firmwareVers );
    return std::make_tuple(__ret, firmwareVers);
  }


  std::tuple<ctre::phoenix::ErrorCode, bool> hasResetOccurred() {
    bool hasReset;
    auto __ret =  c_CANifier_HasResetOccurred(m_handle, &hasReset );
    return std::make_tuple(__ret, hasReset);
  }


  ctre::phoenix::ErrorCode setStatusFramePeriod(int frame, int periodMs, int timeoutMs) {
    
    auto __ret =  c_CANifier_SetStatusFramePeriod(m_handle, frame, periodMs, timeoutMs );
    return __ret;
  }


  std::tuple<ctre::phoenix::ErrorCode, int> getStatusFramePeriod(int frame, int timeoutMs) {
    int periodMs;
    auto __ret =  c_CANifier_GetStatusFramePeriod(m_handle, frame, &periodMs, timeoutMs );
    return std::make_tuple(__ret, periodMs);
  }


  ctre::phoenix::ErrorCode setControlFramePeriod(int frame, int periodMs) {
    
    auto __ret =  c_CANifier_SetControlFramePeriod(m_handle, frame, periodMs );
    return __ret;
  }


};