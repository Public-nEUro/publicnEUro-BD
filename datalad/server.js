const express = require("express");
const path = require("path");
const app = express();

const repoPath = "/root/repo";

app.use(express.static(repoPath));

app.get("/", (req, res) => {
    res.sendFile(path.join(repoPath, "index.html"));
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
