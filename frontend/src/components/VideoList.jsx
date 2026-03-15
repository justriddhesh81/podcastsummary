import { useState } from "react";

function VideoList({ videos, onSelect }) {
  const [activeVideoId, setActiveVideoId] = useState(null);

  if (!videos || videos.length === 0) return null;

  return (
    <div style={styles.container}>
      {videos.map((video) => (
        <div key={video.id} style={styles.card}>
          
          {/* LEFT SIDE */}
          <div style={styles.leftSection}>
            <img
              src={video.thumbnail}
              alt={video.title}
              style={styles.thumbnail}
            />
            <div>
              <h4 style={styles.title}>{video.title}</h4>
              <p style={styles.channel}>{video.channel}</p>
            </div>
          </div>

          {/* RIGHT SIDE - 3 DOT BUTTON */}
          <div style={styles.rightSection}>
            <button
              style={styles.menuButton}
              onClick={() =>
                setActiveVideoId(
                  activeVideoId === video.id ? null : video.id
                )
              }
            >
              ⋮
            </button>

            {/* CONFIRMATION POPUP */}
            {activeVideoId === video.id && (
              <div style={styles.popup}>
                <p>Generate summary?</p>
                <button
                  style={styles.confirmBtn}
                  onClick={() => {
                    setActiveVideoId(null);
                    onSelect(video);
                  }}
                >
                  Yes
                </button>
                <button
                  style={styles.cancelBtn}
                  onClick={() => setActiveVideoId(null)}
                >
                  Cancel
                </button>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

const styles = {
  container: {
    marginTop: "20px",
    display: "flex",
    flexDirection: "column",
    gap: "15px"
  },
  card: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "12px",
    backgroundColor: "#1c1c1c",
    borderRadius: "10px",
    position: "relative"
  },
  leftSection: {
    display: "flex",
    gap: "15px",
    alignItems: "center"
  },
  rightSection: {
    position: "relative"
  },
  thumbnail: {
    width: "140px",
    borderRadius: "8px"
  },
  title: {
    margin: "0 0 5px 0"
  },
  channel: {
    margin: 0,
    color: "#aaa",
    fontSize: "14px"
  },
  menuButton: {
    background: "none",
    border: "none",
    color: "white",
    fontSize: "20px",
    cursor: "pointer"
  },
  popup: {
    position: "absolute",
    right: 0,
    top: "30px",
    backgroundColor: "#2a2a2a",
    padding: "10px",
    borderRadius: "8px",
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    width: "150px",
    zIndex: 10
  },
  confirmBtn: {
    backgroundColor: "#ff0000",
    border: "none",
    color: "white",
    padding: "6px",
    borderRadius: "6px",
    cursor: "pointer"
  },
  cancelBtn: {
    backgroundColor: "#444",
    border: "none",
    color: "white",
    padding: "6px",
    borderRadius: "6px",
    cursor: "pointer"
  }
};

export default VideoList; 