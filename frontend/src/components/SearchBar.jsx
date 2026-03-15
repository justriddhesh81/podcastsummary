import { useState } from "react";

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSubmit = () => {
    if (!query.trim()) return;
    onSearch(query);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSubmit();
    }
  };

  return (
    <div style={styles.container}>
      <input
        type="text"
        placeholder="Search YouTube video or paste link..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        style={styles.input}
      />
      <button style={styles.button} onClick={handleSubmit}>
        Search
      </button>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    gap: "10px",
    marginTop: "40px"
  },
  input: {
    flex: 1,
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    fontSize: "16px"
  },
  button: {
    backgroundColor: "#ff0000",
    color: "white",
    padding: "12px 18px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    fontWeight: "bold"
  }
};

export default SearchBar;