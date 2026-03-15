import { useState } from "react";
import { summarizeVideo } from "../services/api";
import { searchYouTube } from "../services/api";
import Navbar from "../components/Navbar";
import SearchBar from "../components/SearchBar";
import VideoList from "../components/VideoList";
import ModelSelector from "../components/ModelSelector";
import Loader from "../components/Loader";
import SummaryBox from "../components/SummaryBox";

function extractVideoId(url) {
  const match = url.match(/v=([^&]+)/);
  return match ? match[1] : url;
}

function Home() {
  const [videos, setVideos] = useState([]); // search results
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState("bart");

  // Temporary dummy search (until YouTube API added)


const handleSearch = async (query) => {
  try {
    setLoading(true);
    setSummary("");
    setSelectedVideo(null);

    const results = await searchYouTube(query);
    setVideos(results);
  } catch (error) {
    alert("Error searching YouTube");
  } finally {
    setLoading(false);
  }
};

  const handleSelect = (video) => {
    setSelectedVideo(video);
    setSummary("");
  };

  const handleSummarize = async () => {
    if (!selectedVideo) return alert("Select a video first");

    try {
      setLoading(true);
      setSummary("");

      const data = await summarizeVideo(
        selectedVideo.id,
        selectedModel
      );

      setSummary(data.summary);
    } catch (error) {
      alert("Error generating summary");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="container">
        <SearchBar onSearch={handleSearch} />

        <VideoList videos={videos} onSelect={handleSelect} />

        {selectedVideo && (
          <>
            <ModelSelector
              models={["bart", "pegasus", "flan"]}
              selectedModel={selectedModel}
              onChange={setSelectedModel}
            />

            <button
              className="primary-btn"
              style={{ marginTop: "20px" }}
              onClick={handleSummarize}
            >
              Summarize
            </button>
          </>
        )}

        {loading && <Loader />}
        <SummaryBox summary={summary} />
      </div>
    </>
  );
}

export default Home;