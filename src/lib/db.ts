import sqlite3 from 'sqlite3';
import { open, Database } from 'sqlite';
import path from 'path';

let db: Database<sqlite3.Database, sqlite3.Statement> | null = null;

export async function getDbConnection() {
  if (!db) {
    const dbPath = path.join(process.cwd(), 'thinkora.db');
    db = await open({
      filename: dbPath,
      driver: sqlite3.Database,
    });
  }
  return db;
} 