function Navbar() {
  return (
    <nav style={styles.nav}>
      <h2 style={styles.logo}>🎙 Podcast Summarizer</h2>
    </nav>
  );
}

const styles = {
  nav: {
    backgroundColor: "#141414",
    padding: "16px 40px",
    borderBottom: "1px solid #222",
    position: "sticky",
    top: 0,
    zIndex: 1000
  },
  logo: {
    margin: 0,
    color: "#ff0000",
    fontWeight: "bold"
  }
};

export default Navbar;