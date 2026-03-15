function ModelSelector({ models, selectedModel, onChange }) {
  return (
    <div style={styles.container}>
      <label style={styles.label}>Choose Model:</label>
      <select
        value={selectedModel}
        onChange={(e) => onChange(e.target.value)}
        style={styles.select}
      >
        {models.map((model) => (
          <option key={model} value={model}>
            {model.toUpperCase()}
          </option>
        ))}
      </select>
    </div>
  );
}

const styles = {
  container: {
    marginTop: "20px",
    display: "flex",
    alignItems: "center",
    gap: "10px"
  },
  label: {
    fontWeight: "bold"
  },
  select: {
    padding: "8px",
    borderRadius: "6px",
    border: "none"
  }
};

export default ModelSelector;