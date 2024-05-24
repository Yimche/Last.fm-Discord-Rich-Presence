import pylast
import time
import DiscordRPC as RPC

API_KEY = "c70ac96baa4d4d456b3d3de853a3e67b"
API_SECRET = "533fd5c895205ce2994df6fca418fd8b"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)


class LastFmUser:
    def __init__(self, username, cooldown):
        self.username = username
        self.user = network.get_user(username)
        self.cooldown = cooldown

    def now_playing(self, button_state):
        current_track = None
        try:
            current_track = self.user.get_now_playing()
            pass
        except pylast.WSError:
            print("Connection problem at web serice, retrying connection in " +
                  str(self.cooldown)+" seconds")
            pass
        except pylast.NetworkError:
            print("The app couldn't comunicate with last.fm servers, check your internet connection!")
            pass
        except pylast.MalformedResponseError:
            print("Last.fm internal server error!, retrying connection")
            pass

        if current_track is not None:
            track = current_track
            try:
                time_remaining = 0
                title = track.get_title()
                artist = track.get_artist()
                artwork = track.get_cover_image()
                if artwork is None:
                    artwork = 'https://raw.githubusercontent.com/Gust4Oliveira/Last.fm-Discord-Rich-Presence/master/assets/last.fm.png'
                time_remaining = track.get_duration()
            except pylast.WSError:
                pass
            except pylast.NetworkError:
                print(
                    "The app couldn't comunicate with last.fm servers, check your internet connection!")
                pass
            RPC.enable_RPC()
            RPC.update_Status(str(track), title, str(artist), time_remaining, self.username, artwork, button_state)
            time.sleep(self.cooldown+8)
        else:
            print("No song detected, checking again in " +
                  str(self.cooldown)+" seconds")
            RPC.disable_RPC()
        time.sleep(self.cooldown)
