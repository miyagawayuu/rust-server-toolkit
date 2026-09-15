using System;
using System.Globalization;

namespace Oxide.Plugins
{
    [Info("ToolkitSmoke", "miyagawayuu", "0.1.0")]
    [Description("Isolated compatibility fixture for Rust Server Toolkit; not a production plugin.")]
    public class ToolkitSmoke : RustPlugin
    {
        private class Settings
        {
            public double Multiplier = 1.0;
        }

        private Settings settings;

        protected override void LoadDefaultConfig()
        {
            Config.WriteObject(new Settings(), true);
        }

        private void Init()
        {
            settings = Config.ReadObject<Settings>();
            if (settings == null || Math.Abs(settings.Multiplier - 2.0) > 0.00001)
                throw new Exception("TOOLKIT_CONFIG_REJECTED: expected Multiplier=2");
            Puts("TOOLKIT_CONFIG_OK multiplier=" + settings.Multiplier.ToString(CultureInfo.InvariantCulture));
        }

        private void OnServerInitialized()
        {
            Puts("TOOLKIT_SERVER_INITIALIZED");
        }
    }
}
