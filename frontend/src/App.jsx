import { useState } from "react";
import Navbar from "./components/Navbar";
import SearchBar from "./components/SearchBar";
import VideoList from "./components/VideoList";
import ModelSelector from "./components/ModelSelector";
function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);

  return `${minutes}:${secs.toString().padStart(2, "0")}`;
}
function App() {
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [selectedModel, setSelectedModel] = useState("bart");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [sections, setSections] = useState([]);

  const handleSearch = async (query) => {
    try {
      const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY;

      const response = await fetch(
        `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&q=${encodeURIComponent(query)}&key=${API_KEY}`
      );

      const data = await response.json();

      const formattedVideos = data.items.map((item) => ({
        id: item.id.videoId,
        title: item.snippet.title,
        channel: item.snippet.channelTitle,
        thumbnail: item.snippet.thumbnails.medium.url
      }));

      setVideos(formattedVideos);
    } catch (error) {
      console.error("Search failed:", error);
    }
  };

  const handleVideoSelect = async (video) => {
  try {
    setLoading(true);
    setSummary("");
    setSelectedVideo(video);

    const response = await fetch(
      `http://localhost:8000/summarize/${video.id}?model=${selectedModel}`
    );

    const data = await response.json();

    console.log(data);

    setSummary(data.overview);
    setSections(data.section_summaries);

  } catch (error) {
    console.error("Summarization failed:", error);
    alert("Error generating summary");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="app">
      <Navbar />

      <SearchBar onSearch={handleSearch} />

      <ModelSelector
        models={["bart", "flan"]}
        selectedModel={selectedModel}
        onChange={setSelectedModel}
      />

      <VideoList
        videos={videos}
        onSelect={handleVideoSelect}
      />

      {loading && <p>Generating summary...</p>}

      {summary && (
  <div style={{ marginTop: "30px", padding: "20px", background: "#1c1c1c", borderRadius: "10px" }}>
    
    <h3>Overview</h3>
    <p>{summary}</p>

    <h3 style={{ marginTop: "20px" }}>Podcast Highlights</h3>

    {sections.map((sec, i) => (
      <div key={i} style={{ marginBottom: "10px" }}>
        
        <a
          href={`https://youtube.com/watch?v=${selectedVideo?.id}&t=${Math.floor(sec.timestamp)}s`}
          target="_blank"
          rel="noopener noreferrer"
          style={{ color: "#ff0000", fontWeight: "bold", marginRight: "10px" }}
        >
          {formatTime(sec.timestamp)}
        </a>

        {sec.summary}

      </div>
    ))}

  </div>
)}
    </div>
  );
}

export default App;