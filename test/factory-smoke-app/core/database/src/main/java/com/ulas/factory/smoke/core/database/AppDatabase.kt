package com.ulas.factory.smoke.core.database

import androidx.room.Database
import androidx.room.RoomDatabase
import com.ulas.factory.smoke.core.database.entity.SyncQueueEntity

@Database(entities = [SyncQueueEntity::class], version = 1, exportSchema = true)
abstract class AppDatabase : RoomDatabase()
