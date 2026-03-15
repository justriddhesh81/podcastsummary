import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const summarizeVideo = async (videoId, model = "bart") => {
  const response = await axios.get(
    `${API_BASE}/summarize/${videoId}?model=${model}`
  );
  return response.data;
};

// 🔎 Real YouTube search
export const searchYouTube = async (query) => {
  const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY;

  const response = await axios.get(
    "https://www.googleapis.com/youtube/v3/search",
    {
      params: {
        part: "snippet",
        q: query,
        key: API_KEY,
        maxResults: 5,
        type: "video"
      }
    }
  );

  return response.data.items.map((item) => ({
    id: item.id.videoId,
    title: item.snippet.title,
    channel: item.snippet.channelTitle,
    thumbnail: item.snippet.thumbnails.medium.url
  }));
};