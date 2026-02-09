from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """
    Extracts video ID from a YouTube URL.
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def collect_youtube_transcript(video_url):
    """
    Fetches transcript for a given YouTube video URL.
    """
    video_id = get_video_id(video_url)
    if not video_id:
        print(f"Error: Invalid YouTube URL {video_url}")
        return None

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine transcript into a single string
        full_text = " ".join([t['text'] for t in transcript_list])
        return full_text
    except Exception as e:
        print(f"Error fetching transcript for {video_url}: {e}")
        # Investigate specific error types here if needed (e.g. key error)
        return None

if __name__ == "__main__":
    # Test execution
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Rick Roll for testing :)
    transcript = collect_youtube_transcript(test_url)
    if transcript:
        print(f"Transcript length: {len(transcript)} characters")
        print(f"Preview: {transcript[:100]}...")
    else:
        print("Failed to fetch transcript.")
