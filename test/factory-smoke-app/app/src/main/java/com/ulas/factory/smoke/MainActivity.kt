package com.ulas.factory.smoke

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import dagger.hilt.android.AndroidEntryPoint
import com.ulas.factory.smoke.core.designsystem.theme.FactorySmokeTheme
import com.ulas.factory.smoke.feature.home.presentation.HomeScreen

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            FactorySmokeTheme {
                HomeScreen()
            }
        }
    }
}
