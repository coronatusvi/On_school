import "package:flutter/foundation.dart";
import "package:sqflite/sqflite.dart" as sql;

class SQLHelper {
  static Future<void> createTables(sql.Database database) async {
    await database.execute("""CREATE TABLE items(
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      title TEXT,
      description TEXT,
      createAT TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """);
    await database.execute("""CREATE TABLE students (
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      studentCode TEXT,
      name TEXT,
      className TEXT,
      course TEXT,
      createAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """);
  }

  static Future<int> createStudent(Map<String, dynamic> data) async {
    final db = await SQLHelper.db();
    final id = await db.insert('students', data,
        conflictAlgorithm: sql.ConflictAlgorithm.replace);
    return id;
  }

  static Future<List<Map<String, dynamic>>> getStudents() async {
    final db = await SQLHelper.db();
    return db.query('students', orderBy: "id");
  }

  static Future<void> deleteStudent(int id) async {
    final db = await SQLHelper.db();
    await db.delete('students', where: "id = ?", whereArgs: [id]);
  }

  static Future<List<Map<String, dynamic>>> searchStudents(
      String keyword) async {
    final db = await SQLHelper.db();
    return db
        .query('students', where: "name LIKE ?", whereArgs: ['%$keyword%']);
  }

  static Future<sql.Database> db() async {
    return sql.openDatabase(
      'dbestech.db',
      version: 1,
      onCreate: (sql.Database database, int version) async {
        await createTables(database);
      },
    );
  }

  static Future<int> createItem(String title, String? description) async {
    final db = await SQLHelper.db();
    final data = {'title': title, 'description': description};

    final id = await db.insert('items', data,
        conflictAlgorithm: sql.ConflictAlgorithm.replace);
    return id;
  }

  static Future<List<Map<String, dynamic>>> getItems() async {
    final db = await SQLHelper.db();
    return db.query('items', orderBy: "id");
  }

  static Future<List<Map<String, dynamic>>> getItem(int id) async {
    final db = await SQLHelper.db();
    return db.query('items', where: "id = ?", whereArgs: [id], limit: 1);
  }

  static Future<int> updateItem(
      int id, String title, String? description) async {
    final db = await SQLHelper.db();

    final data = {
      'title': title,
      'description': description,
      'createAt': DateTime.now().toString(),
    };

    final result =
        await db.update("items", data, where: "id = ?", whereArgs: [id]);

    return result;
  }

  static Future<void> deleteItem(int id) async {
    final db = await SQLHelper.db();

    try {
      await db.delete('items', where: "id = ?", whereArgs: [id]);
    } catch (err) {
      debugPrint("Co loi khi xoa item: $err");
    }
  }
}
