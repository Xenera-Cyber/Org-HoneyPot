// src/context/SettingsContext.tsx (Updated)
import {
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";

export type ThemeMode = "dark" | "light" | "ocean" | "midnight" | "forest";

export interface AuditEntry {
  time: string;
  field: string;
  value: string;
}

export interface SettingsContextType {
  // Theme
  theme: ThemeMode;
  setTheme: (v: ThemeMode) => void;
  
  // All other settings...
  refreshRate: number;
  setRefreshRate: (v: number) => void;
  
  aiEnabled: boolean;
  setAIEnabled: (v: boolean) => void;
  
  ragEnabled: boolean;
  setRAGEnabled: (v: boolean) => void;
  
  guardrailsEnabled: boolean;
  setGuardrailsEnabled: (v: boolean) => void;
  
  sshEnabled: boolean;
  setSSHEnabled: (v: boolean) => void;
  
  httpEnabled: boolean;
  setHTTPEnabled: (v: boolean) => void;
  
  ftpEnabled: boolean;
  setFTPEnabled: (v: boolean) => void;
  
  maxConcurrentSessions: number;
  setMaxConcurrentSessions: (v: number) => void;
  
  sessionTimeoutMinutes: number;
  setSessionTimeoutMinutes: (v: number) => void;
  
  logRetentionDays: number;
  setLogRetentionDays: (v: number) => void;
  
  maxCommandsPerSession: number;
  setMaxCommandsPerSession: (v: number) => void;
  
  graphHistoryHours: number;
  setGraphHistoryHours: (v: number) => void;
  
  autoRefresh: boolean;
  setAutoRefresh: (v: boolean) => void;
  
  language: string;
  setLanguage: (v: string) => void;
  
  timezone: string;
  setTimezone: (v: string) => void;
  
  // AI Settings
  personality: string;
  setPersonality: (v: string) => void;
  
  model: string;
  setModel: (v: string) => void;
  
  confidenceThreshold: number;
  setConfidenceThreshold: (v: number) => void;
  
  temperature: number;
  setTemperature: (v: number) => void;
  
  maxContext: number;
  setMaxContext: (v: number) => void;
  
  maxResponseLength: number;
  setMaxResponseLength: (v: number) => void;
  
  // Dashboard Visual Settings
  showAttackRoutes: boolean;
  setShowAttackRoutes: (v: boolean) => void;
  
  animations: boolean;
  setAnimations: (v: boolean) => void;
  
  compactMode: boolean;
  setCompactMode: (v: boolean) => void;
  
  showLastUpdated: boolean;
  setShowLastUpdated: (v: boolean) => void;
  
  // Notification Settings
  desktopNotifications: boolean;
  setDesktopNotifications: (v: boolean) => void;
  
  emailNotifications: boolean;
  setEmailNotifications: (v: boolean) => void;
  
  telegramNotifications: boolean;
  setTelegramNotifications: (v: boolean) => void;
  
  slackNotifications: boolean;
  setSlackNotifications: (v: boolean) => void;
  
  minimumAlertLevel: string;
  setMinimumAlertLevel: (v: string) => void;
  
  alertEmail: string;
  setAlertEmail: (v: string) => void;
  
  telegramChat: string;
  setTelegramChat: (v: string) => void;
  
  telegramBotToken: string;
  setTelegramBotToken: (v: string) => void;
  
  slackWebhook: string;
  setSlackWebhook: (v: string) => void;
  
  // Security Settings
  twoFactor: boolean;
  setTwoFactor: (v: boolean) => void;
  
  autoLogout: boolean;
  setAutoLogout: (v: boolean) => void;
  
  auditLogs: boolean;
  setAuditLogs: (v: boolean) => void;
  
  lockout: boolean;
  setLockout: (v: boolean) => void;
  
  sessionTimeout: number;
  setSessionTimeout: (v: number) => void;
  
  allowedIP: string;
  setAllowedIP: (v: string) => void;
  
  defaultRole: string;
  setDefaultRole: (v: string) => void;
  
  auditLog: AuditEntry[];
  clearAuditLog: () => void;
}

const SettingsContext = createContext<SettingsContextType | null>(null);

const STORAGE_KEY = "xynera.settings.v2";

const DEFAULTS = {
  theme: "dark" as ThemeMode,
  refreshRate: 5,
  aiEnabled: true,
  ragEnabled: true,
  guardrailsEnabled: true,
  sshEnabled: true,
  httpEnabled: true,
  ftpEnabled: true,
  maxConcurrentSessions: 50,
  sessionTimeoutMinutes: 30,
  logRetentionDays: 30,
  maxCommandsPerSession: 250,
  graphHistoryHours: 3,
  autoRefresh: true,
  language: "English",
  timezone: "UTC +05:30",
  personality: "auto",
  model: "llama-3.3-70b-versatile",
  confidenceThreshold: 85,
  temperature: 0.3,
  maxContext: 4096,
  maxResponseLength: 1024,
  showAttackRoutes: true,
  animations: true,
  compactMode: false,
  showLastUpdated: true,
  desktopNotifications: true,
  emailNotifications: false,
  telegramNotifications: false,
  slackNotifications: false,
  minimumAlertLevel: "High",
  alertEmail: "",
  telegramChat: "",
  telegramBotToken: "",
  slackWebhook: "",
  twoFactor: false,
  autoLogout: true,
  auditLogs: true,
  lockout: true,
  sessionTimeout: 30,
  allowedIP: "",
  defaultRole: "Administrator",
};

type PersistedSettings = typeof DEFAULTS;

function loadPersisted(): PersistedSettings {
  if (typeof window === "undefined") return DEFAULTS;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEFAULTS;
    return { ...DEFAULTS, ...JSON.parse(raw) };
  } catch {
    return DEFAULTS;
  }
}

export function SettingsProvider({ children }: { children: React.ReactNode }) {
  const initial = useRef(loadPersisted()).current;
  
  const [theme, setThemeState] = useState<ThemeMode>(initial.theme);
  const [refreshRate, setRefreshRateState] = useState(initial.refreshRate);
  const [aiEnabled, setAIEnabledState] = useState(initial.aiEnabled);
  const [ragEnabled, setRAGEnabledState] = useState(initial.ragEnabled);
  const [guardrailsEnabled, setGuardrailsEnabledState] = useState(initial.guardrailsEnabled);
  const [sshEnabled, setSSHEnabledState] = useState(initial.sshEnabled);
  const [httpEnabled, setHTTPEnabledState] = useState(initial.httpEnabled);
  const [ftpEnabled, setFTPEnabledState] = useState(initial.ftpEnabled);
  const [maxConcurrentSessions, setMaxConcurrentSessionsState] = useState(initial.maxConcurrentSessions);
  const [sessionTimeoutMinutes, setSessionTimeoutMinutesState] = useState(initial.sessionTimeoutMinutes);
  const [logRetentionDays, setLogRetentionDaysState] = useState(initial.logRetentionDays);
  const [maxCommandsPerSession, setMaxCommandsPerSessionState] = useState(initial.maxCommandsPerSession);
  const [graphHistoryHours, setGraphHistoryHoursState] = useState(initial.graphHistoryHours);
  const [autoRefresh, setAutoRefreshState] = useState(initial.autoRefresh);
  const [language, setLanguageState] = useState(initial.language);
  const [timezone, setTimezoneState] = useState(initial.timezone);
  const [personality, setPersonalityState] = useState(initial.personality);
  const [model, setModelState] = useState(initial.model);
  const [confidenceThreshold, setConfidenceThresholdState] = useState(initial.confidenceThreshold);
  const [temperature, setTemperatureState] = useState(initial.temperature);
  const [maxContext, setMaxContextState] = useState(initial.maxContext);
  const [maxResponseLength, setMaxResponseLengthState] = useState(initial.maxResponseLength);
  const [showAttackRoutes, setShowAttackRoutesState] = useState(initial.showAttackRoutes);
  const [animations, setAnimationsState] = useState(initial.animations);
  const [compactMode, setCompactModeState] = useState(initial.compactMode);
  const [showLastUpdated, setShowLastUpdatedState] = useState(initial.showLastUpdated);
  const [desktopNotifications, setDesktopNotificationsState] = useState(initial.desktopNotifications);
  const [emailNotifications, setEmailNotificationsState] = useState(initial.emailNotifications);
  const [telegramNotifications, setTelegramNotificationsState] = useState(initial.telegramNotifications);
  const [slackNotifications, setSlackNotificationsState] = useState(initial.slackNotifications);
  const [minimumAlertLevel, setMinimumAlertLevelState] = useState(initial.minimumAlertLevel);
  const [alertEmail, setAlertEmailState] = useState(initial.alertEmail);
  const [telegramChat, setTelegramChatState] = useState(initial.telegramChat);
  const [telegramBotToken, setTelegramBotTokenState] = useState(initial.telegramBotToken);
  const [slackWebhook, setSlackWebhookState] = useState(initial.slackWebhook);
  const [twoFactor, setTwoFactorState] = useState(initial.twoFactor);
  const [autoLogout, setAutoLogoutState] = useState(initial.autoLogout);
  const [auditLogs, setAuditLogsState] = useState(initial.auditLogs);
  const [lockout, setLockoutState] = useState(initial.lockout);
  const [sessionTimeout, setSessionTimeoutState] = useState(initial.sessionTimeout);
  const [allowedIP, setAllowedIPState] = useState(initial.allowedIP);
  const [defaultRole, setDefaultRoleState] = useState(initial.defaultRole);
  const [auditLog, setAuditLog] = useState<AuditEntry[]>([]);

  function logChange(field: string, value: unknown) {
    setAuditLog((prev) =>
      [
        {
          time: new Date().toLocaleTimeString(),
          field,
          value: String(value),
        },
        ...prev,
      ].slice(0, 50)
    );
  }

  function clearAuditLog() {
    setAuditLog([]);
  }

  function tracked<V>(field: string, setter: (v: V) => void) {
    return (v: V) => {
      setter(v);
      logChange(field, v);
    };
  }

  const setTheme = tracked("theme", setThemeState);
  const setRefreshRate = tracked("refreshRate", setRefreshRateState);
  const setAIEnabled = tracked("aiEnabled", setAIEnabledState);
  const setRAGEnabled = tracked("ragEnabled", setRAGEnabledState);
  const setGuardrailsEnabled = tracked("guardrailsEnabled", setGuardrailsEnabledState);
  const setSSHEnabled = tracked("sshEnabled", setSSHEnabledState);
  const setHTTPEnabled = tracked("httpEnabled", setHTTPEnabledState);
  const setFTPEnabled = tracked("ftpEnabled", setFTPEnabledState);
  const setMaxConcurrentSessions = tracked("maxConcurrentSessions", setMaxConcurrentSessionsState);
  const setSessionTimeoutMinutes = tracked("sessionTimeoutMinutes", setSessionTimeoutMinutesState);
  const setLogRetentionDays = tracked("logRetentionDays", setLogRetentionDaysState);
  const setMaxCommandsPerSession = tracked("maxCommandsPerSession", setMaxCommandsPerSessionState);
  const setGraphHistoryHours = tracked("graphHistoryHours", setGraphHistoryHoursState);
  const setAutoRefresh = tracked("autoRefresh", setAutoRefreshState);
  const setLanguage = tracked("language", setLanguageState);
  const setTimezone = tracked("timezone", setTimezoneState);
  const setPersonality = tracked("personality", setPersonalityState);
  const setModel = tracked("model", setModelState);
  const setConfidenceThreshold = tracked("confidenceThreshold", setConfidenceThresholdState);
  const setTemperature = tracked("temperature", setTemperatureState);
  const setMaxContext = tracked("maxContext", setMaxContextState);
  const setMaxResponseLength = tracked("maxResponseLength", setMaxResponseLengthState);
  const setShowAttackRoutes = tracked("showAttackRoutes", setShowAttackRoutesState);
  const setAnimations = tracked("animations", setAnimationsState);
  const setCompactMode = tracked("compactMode", setCompactModeState);
  const setShowLastUpdated = tracked("showLastUpdated", setShowLastUpdatedState);
  const setDesktopNotifications = tracked("desktopNotifications", setDesktopNotificationsState);
  const setEmailNotifications = tracked("emailNotifications", setEmailNotificationsState);
  const setTelegramNotifications = tracked("telegramNotifications", setTelegramNotificationsState);
  const setSlackNotifications = tracked("slackNotifications", setSlackNotificationsState);
  const setMinimumAlertLevel = tracked("minimumAlertLevel", setMinimumAlertLevelState);
  const setAlertEmail = tracked("alertEmail", setAlertEmailState);
  const setTelegramChat = tracked("telegramChat", setTelegramChatState);
  const setTelegramBotToken = tracked("telegramBotToken", setTelegramBotTokenState);
  const setSlackWebhook = tracked("slackWebhook", setSlackWebhookState);
  const setTwoFactor = tracked("twoFactor", setTwoFactorState);
  const setAutoLogout = tracked("autoLogout", setAutoLogoutState);
  const setAuditLogsSetting = tracked("auditLogs", setAuditLogsState);
  const setLockout = tracked("lockout", setLockoutState);
  const setSessionTimeout = tracked("sessionTimeout", setSessionTimeoutState);
  const setAllowedIP = tracked("allowedIP", setAllowedIPState);
  const setDefaultRole = tracked("defaultRole", setDefaultRoleState);

  // Persist to localStorage
  useEffect(() => {
    const snapshot: PersistedSettings = {
      theme,
      refreshRate,
      aiEnabled,
      ragEnabled,
      guardrailsEnabled,
      sshEnabled,
      httpEnabled,
      ftpEnabled,
      maxConcurrentSessions,
      sessionTimeoutMinutes,
      logRetentionDays,
      maxCommandsPerSession,
      graphHistoryHours,
      autoRefresh,
      language,
      timezone,
      personality,
      model,
      confidenceThreshold,
      temperature,
      maxContext,
      maxResponseLength,
      showAttackRoutes,
      animations,
      compactMode,
      showLastUpdated,
      desktopNotifications,
      emailNotifications,
      telegramNotifications,
      slackNotifications,
      minimumAlertLevel,
      alertEmail,
      telegramChat,
      telegramBotToken,
      slackWebhook,
      twoFactor,
      autoLogout,
      auditLogs,
      lockout,
      sessionTimeout,
      allowedIP,
      defaultRole,
    };
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot));
    } catch {
      // localStorage unavailable
    }
  }, [
    theme,
    refreshRate,
    aiEnabled,
    ragEnabled,
    guardrailsEnabled,
    sshEnabled,
    httpEnabled,
    ftpEnabled,
    maxConcurrentSessions,
    sessionTimeoutMinutes,
    logRetentionDays,
    maxCommandsPerSession,
    graphHistoryHours,
    autoRefresh,
    language,
    timezone,
    personality,
    model,
    confidenceThreshold,
    temperature,
    maxContext,
    maxResponseLength,
    showAttackRoutes,
    animations,
    compactMode,
    showLastUpdated,
    desktopNotifications,
    emailNotifications,
    telegramNotifications,
    slackNotifications,
    minimumAlertLevel,
    alertEmail,
    telegramChat,
    telegramBotToken,
    slackWebhook,
    twoFactor,
    autoLogout,
    auditLogs,
    lockout,
    sessionTimeout,
    allowedIP,
    defaultRole,
  ]);

  // Apply theme to document
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  // Apply compact mode
  useEffect(() => {
    document.documentElement.classList.toggle("compact", compactMode);
  }, [compactMode]);

  // Apply animations mode
  useEffect(() => {
    document.documentElement.classList.toggle("no-animations", !animations);
  }, [animations]);

  return (
    <SettingsContext.Provider
      value={{
        theme,
        refreshRate,
        aiEnabled,
        ragEnabled,
        guardrailsEnabled,
        sshEnabled,
        httpEnabled,
        ftpEnabled,
        maxConcurrentSessions,
        sessionTimeoutMinutes,
        logRetentionDays,
        maxCommandsPerSession,
        graphHistoryHours,
        autoRefresh,
        language,
        timezone,
        personality,
        model,
        confidenceThreshold,
        temperature,
        maxContext,
        maxResponseLength,
        showAttackRoutes,
        animations,
        compactMode,
        showLastUpdated,
        desktopNotifications,
        emailNotifications,
        telegramNotifications,
        slackNotifications,
        minimumAlertLevel,
        alertEmail,
        telegramChat,
        telegramBotToken,
        slackWebhook,
        twoFactor,
        autoLogout,
        auditLogs,
        lockout,
        sessionTimeout,
        allowedIP,
        defaultRole,
        auditLog,
        clearAuditLog,
        setTheme,
        setRefreshRate,
        setAIEnabled,
        setRAGEnabled,
        setGuardrailsEnabled,
        setSSHEnabled,
        setHTTPEnabled,
        setFTPEnabled,
        setMaxConcurrentSessions,
        setSessionTimeoutMinutes,
        setLogRetentionDays,
        setMaxCommandsPerSession,
        setGraphHistoryHours,
        setAutoRefresh,
        setLanguage,
        setTimezone,
        setPersonality,
        setModel,
        setConfidenceThreshold,
        setTemperature,
        setMaxContext,
        setMaxResponseLength,
        setShowAttackRoutes,
        setAnimations,
        setCompactMode,
        setShowLastUpdated,
        setDesktopNotifications,
        setEmailNotifications,
        setTelegramNotifications,
        setSlackNotifications,
        setMinimumAlertLevel,
        setAlertEmail,
        setTelegramChat,
        setTelegramBotToken,
        setSlackWebhook,
        setTwoFactor,
        setAutoLogout,
        setAuditLogs: setAuditLogsSetting,
        setLockout,
        setSessionTimeout,
        setAllowedIP,
        setDefaultRole,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettingsContext() {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error("useSettingsContext must be used inside SettingsProvider");
  }
  return context;
}