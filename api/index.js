const express = require('express');
const pool = require('./db');
const app = express();

app.use(express.json());

// API: Mendapatkan semua armada (vehicle)
app.get('/vehicle', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM vehicle');
    res.json(rows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// API: Mendapatkan riwayat posisi bus tertentu berdasarkan vehicle_id
app.get('/history/:vehicle_id', async (req, res) => {
  const { vehicle_id } = req.params;
  try {
    const { rows } = await pool.query(
      'SELECT * FROM history WHERE vehicle_id = $1 ORDER BY gpsdatetime DESC',
      [vehicle_id]
    );
    res.json(rows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Konfigurasi IP dan Port
const PORT = process.env.PORT || 3001;
const HOST = process.env.HOST || '  ';

// Menjalankan server
app.listen(PORT, HOST, () => {
  console.log(`Server berjalan di http://${HOST}:${PORT}/vehicles`);
});
