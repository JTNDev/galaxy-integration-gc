using System;
using System.Diagnostics;
using System.Xml;
using System.IO;
namespace TimeTracker
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            string path = Path.Combine(Environment.GetEnvironmentVariable("LocalAppData"), @"GOG.com\Galaxy\plugins\installed\dolphin_gc_6804a766-c1fd-48cf-9a8b-8661a970a6cb\gametimes.xml");
            string[] arguments = Environment.GetCommandLineArgs();
            string game_id = arguments[1];
            bool is_dolphin_running()
            {
                Process[] pname = Process.GetProcessesByName("dolphin");
                if (pname.Length != 0)
                {
                    return true;
                }
                return false;
            }

            DateTime startingTime = DateTime.Now;
            while (is_dolphin_running())
            {
                System.Threading.Thread.Sleep(100);
            }
            XmlDocument Document;
            Document = new XmlDocument();
            Document.Load(path);
            XmlNode root = Document.SelectSingleNode("games");
            foreach (XmlNode game in root.SelectNodes("game"))
            {
                if (game_id == game.SelectSingleNode("id").InnerText)
                {
                    long previous_time = 0;
                    if (game.SelectSingleNode("time").InnerText != null)
                    {
                        previous_time = Convert.ToInt64(game.SelectSingleNode("time").InnerText);
                    }
                    TimeSpan timeDifference = DateTime.Now - startingTime;

                    string game_time = Convert.ToString(Convert.ToInt64(timeDifference.TotalSeconds + previous_time));
                    game.SelectSingleNode("time").InnerText = game_time;
                    Int32 unixTimestamp = (Int32)(DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1))).TotalSeconds;

                    game.SelectSingleNode("lasttimeplayed").InnerText = Convert.ToString(unixTimestamp);
                }
            }
            Document.Save(path);
        }
    }
}
