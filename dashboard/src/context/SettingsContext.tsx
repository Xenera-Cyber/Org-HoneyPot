import {
    createContext,
    useContext,
    useState,
} from "react";

export interface SettingsContextType {
    theme: "Dark" | "Light";
    refreshRate: number;
    aiEnabled: boolean;
    ragEnabled: boolean;
    guardrailsEnabled: boolean;
    sshEnabled: boolean;
    httpEnabled: boolean;
    ftpEnabled: boolean;
    autoRefresh: boolean;
    language: string;
    timezone: string;

    // NEW EXTENDED AI FIELDS
    personality: string;
    model: string;
    confidenceThreshold: number;
    temperature: number;
    maxContext: number;
    maxResponseLength: number;

    // NEW EXTENDED DASHBOARD VISUAL FIELDS
    showAttackRoutes: boolean;
    animations: boolean;
    compactMode: boolean;
    showLastUpdated: boolean;

    // NEW NOTIFICATION FIELDS
    desktopNotifications: boolean;
    emailNotifications: boolean;
    telegramNotifications: boolean;
    slackNotifications: boolean;
    minimumAlertLevel: string;
    alertEmail: string;
    telegramChat: string;
    slackWebhook: string;

    // SECURITY FIELDS
    twoFactor: boolean;
    autoLogout: boolean;
    auditLogs: boolean;
    lockout: boolean;
    sessionTimeout: number;
    allowedIP: string;
    defaultRole: string;

    setTheme: (v: "Dark" | "Light") => void;
    setRefreshRate: (v: number) => void;
    setAIEnabled: (v: boolean) => void;
    setRAGEnabled: (v: boolean) => void;
    setGuardrailsEnabled: (v: boolean) => void;
    setSSHEnabled: (v: boolean) => void;
    setHTTPEnabled: (v: boolean) => void;
    setFTPEnabled: (v: boolean) => void;
    setAutoRefresh: (v: boolean) => void;
    setLanguage: (v: string) => void;
    setTimezone: (v: string) => void;

    // NEW EXTENDED AI SETTERS
    setPersonality: (v: string) => void;
    setModel: (v: string) => void;
    setConfidenceThreshold: (v: number) => void;
    setTemperature: (v: number) => void;
    setMaxContext: (v: number) => void;
    setMaxResponseLength: (v: number) => void;

    // NEW EXTENDED DASHBOARD VISUAL SETTERS
    setShowAttackRoutes: (v: boolean) => void;
    setAnimations: (v: boolean) => void;
    setCompactMode: (v: boolean) => void;
    setShowLastUpdated: (v: boolean) => void;

    // NEW NOTIFICATION SETTERS
    setDesktopNotifications: (v: boolean) => void;
    setEmailNotifications: (v: boolean) => void;
    setTelegramNotifications: (v: boolean) => void;
    setSlackNotifications: (v: boolean) => void;
    setMinimumAlertLevel: (v: string) => void;
    setAlertEmail: (v: string) => void;
    setTelegramChat: (v: string) => void;
    setSlackWebhook: (v: string) => void;

    // SECURITY SETTERS
    setTwoFactor: (v: boolean) => void;
    setAutoLogout: (v: boolean) => void;
    setAuditLogs: (v: boolean) => void;
    setLockout: (v: boolean) => void;
    setSessionTimeout: (v: number) => void;
    setAllowedIP: (v: string) => void;
    setDefaultRole: (v: string) => void;
}

const SettingsContext =
    createContext<SettingsContextType | null>(null);

export function SettingsProvider({
    children,
}: {
    children: React.ReactNode;
}) {
    const [theme, setTheme] =
        useState<"Dark" | "Light">("Dark");
    const [refreshRate, setRefreshRate] =
        useState(5);
    const [aiEnabled, setAIEnabled] =
        useState(true);
    const [ragEnabled, setRAGEnabled] =
        useState(true);
    const [guardrailsEnabled, setGuardrailsEnabled] =
        useState(true);
    const [sshEnabled, setSSHEnabled] =
        useState(true);
    const [httpEnabled, setHTTPEnabled] =
        useState(true);
    const [ftpEnabled, setFTPEnabled] =
        useState(true);
    const [autoRefresh, setAutoRefresh] =
        useState(true);
    const [language, setLanguage] =
        useState("English");
    const [timezone, setTimezone] =
        useState("UTC +05:30");

    // STATE HOOKS FOR AI CONFIGURATIONS
    const [personality, setPersonality] = useState("Balanced");
    const [model, setModel] = useState("Llama-3");
    const [confidenceThreshold, setConfidenceThreshold] = useState(85);
    const [temperature, setTemperature] = useState(0.3);
    const [maxContext, setMaxContext] = useState(4096);
    const [maxResponseLength, setMaxResponseLength] = useState(1024);

    // NEW STATE HOOKS FOR DASHBOARD SETTINGS
    const [showAttackRoutes, setShowAttackRoutes] = useState(true);
    const [animations, setAnimations] = useState(true);
    const [compactMode, setCompactMode] = useState(false);
    const [showLastUpdated, setShowLastUpdated] = useState(true);

    // NOTIFICATION CHANNELS STATE
    const [desktopNotifications, setDesktopNotifications] = useState(true);
    const [emailNotifications, setEmailNotifications] = useState(false);
    const [telegramNotifications, setTelegramNotifications] = useState(true);
    const [slackNotifications, setSlackNotifications] = useState(false);
    const [minimumAlertLevel, setMinimumAlertLevel] = useState("High");
    const [alertEmail, setAlertEmail] = useState("");
    const [telegramChat, setTelegramChat] = useState("");
    const [slackWebhook, setSlackWebhook] = useState("");

    // SECURITY CONFIGURATION STATE
    const [twoFactor, setTwoFactor] = useState(false);
    const [autoLogout, setAutoLogout] = useState(true);
    const [auditLogs, setAuditLogs] = useState(true);
    const [lockout, setLockout] = useState(true);
    const [sessionTimeout, setSessionTimeout] = useState(30);
    const [allowedIP, setAllowedIP] = useState("");
    const [defaultRole, setDefaultRole] = useState("Administrator");

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
                autoRefresh,
                language,
                timezone,

                // EXPOSED AI STATE
                personality,
                model,
                confidenceThreshold,
                temperature,
                maxContext,
                maxResponseLength,

                // EXPOSED DASHBOARD VISUAL STATE
                showAttackRoutes,
                animations,
                compactMode,
                showLastUpdated,

                // EXPOSED NOTIFICATION STATE
                desktopNotifications,
                emailNotifications,
                telegramNotifications,
                slackNotifications,
                minimumAlertLevel,
                alertEmail,
                telegramChat,
                slackWebhook,

                // EXPOSED SECURITY STATE
                twoFactor,
                autoLogout,
                auditLogs,
                lockout,
                sessionTimeout,
                allowedIP,
                defaultRole,

                setTheme,
                setRefreshRate,
                setAIEnabled,
                setRAGEnabled,
                setGuardrailsEnabled,
                setSSHEnabled,
                setHTTPEnabled,
                setFTPEnabled,
                setAutoRefresh,
                setLanguage,
                setTimezone,

                // EXPOSED AI SETTERS
                setPersonality,
                setModel,
                setConfidenceThreshold,
                setTemperature,
                setMaxContext,
                setMaxResponseLength,

                // EXPOSED DASHBOARD VISUAL SETTERS
                setShowAttackRoutes,
                setAnimations,
                setCompactMode,
                setShowLastUpdated,

                // EXPOSED NOTIFICATION SETTERS
                setDesktopNotifications,
                setEmailNotifications,
                setTelegramNotifications,
                setSlackNotifications,
                setMinimumAlertLevel,
                setAlertEmail,
                setTelegramChat,
                setSlackWebhook,

                // EXPOSED SECURITY SETTERS
                setTwoFactor,
                setAutoLogout,
                setAuditLogs,
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
        throw new Error(
            "useSettingsContext must be used inside SettingsProvider"
        );
    }

    return context;
}