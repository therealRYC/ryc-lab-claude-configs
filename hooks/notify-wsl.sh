#!/bin/bash
# Created: 2026-02-23
# Last updated: 2026-02-23 — Use jq for JSON parsing

# Sends a Windows toast notification from WSL2 via powershell.exe.
# Reads JSON from stdin to extract the notification title.
# Falls back to a generic message if parsing fails.
#
# Exits 0 always — notification failures should never block Claude.

INPUT=$(cat)
TITLE=$(echo "$INPUT" | jq -r '.title // "Needs attention"')

# Use PowerShell BurntToast module if available, otherwise use basic .NET toast
if command -v powershell.exe &>/dev/null; then
    powershell.exe -Command "
        try {
            \$null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
            \$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
            \$text = \$template.GetElementsByTagName('text')
            \$text[0].AppendChild(\$template.CreateTextNode('Claude Code')) | Out-Null
            \$text[1].AppendChild(\$template.CreateTextNode('$TITLE')) | Out-Null
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show([Windows.UI.Notifications.ToastNotification]::new(\$template))
        } catch {
            # Silently fail — notification is best-effort
        }
    " 2>/dev/null
fi

exit 0
