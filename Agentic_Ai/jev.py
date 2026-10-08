from typesafe_sdk import Choice, TypeSafeClient


client = TypeSafeClient()


# -------------------------
# Our application tools
# -------------------------

def play_song(song: str):
    print(f"🎵 PLAY SONG: {song}")
    # Later:
    # - Spotify API
    # - YouTube Music
    # - local player
    # - VLC
    return {
        "tool": "play_song",
        "song": song,
        "status": "started"
    }


def open_youtube(query: str):
    print(f"▶️ OPEN YOUTUBE: {query}")

    # Later we can actually open/search YouTube.
    return {
        "tool": "open_youtube",
        "query": query,
        "status": "opened"
    }


# -------------------------
# User request
# -------------------------

user_request = "Play Blinding Lights by The Weeknd"


# -------------------------
# Ask Jev
# -------------------------

response = client.system_one(
    state=user_request,
    questions={
        "tool": Choice(
            instructions=(
                "Which tool should handle this user request?"
            ),
            criteria={
                "play_song": (
                    "Use when the user wants to play a specific song "
                    "or music."
                ),
                "open_youtube": (
                    "Use when the user wants to search, open, or watch "
                    "something on YouTube."
                ),
            },
        )
    },
)


# -------------------------
# Structured Jev result
# -------------------------

answer = response.answers["tool"]

print("\nJEV RESULT")
print("----------")
print("Choice:", answer.choice)
print("Confidence:", answer.confidence)
print("Probabilities:", answer.probabilities)


# -------------------------
# Application routing
# -------------------------

if answer.choice == "play_song":
    result = play_song(user_request)

elif answer.choice == "open_youtube":
    result = open_youtube(user_request)

else:
    result = {
        "status": "unknown_tool"
    }


print("\nTOOL RESULT")
print("-----------")
print(result)