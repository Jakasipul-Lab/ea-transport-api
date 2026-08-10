const { Pool } = require('pg');
require('dotenv').config({ override: true });

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

async function run() {
  try {
    const res = await pool.query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';");
    console.log('Tables:', res.rows);
  } catch (err) {
    console.error('Error:', err.message);
  } finally {
    await pool.end();
  }
}

run();
