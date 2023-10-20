package com.linshaoqin.myapp.main

import android.content.res.Resources
import android.os.Bundle
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.AppBarConfiguration
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.R

/**
 * my android demo app
 * see [feishu docs](https://cm0nlh86eu.feishu.cn/wiki/YoHBwLrGFiEu8ckIC8TcEPPSnEd)
 */
class MainActivity : AppCompatActivity() {
    private var appBarConfiguration : AppBarConfiguration? = null
    private val mainActivityVM: MainActivityViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setNavConfig()
    }

    private fun setNavConfig() {
        val host: NavHostFragment = supportFragmentManager
            .findFragmentById(R.id.nav_host_main_fragment) as? NavHostFragment? ?: return

        val navController = host.navController

        appBarConfiguration = AppBarConfiguration(navController.graph)

        navController.addOnDestinationChangedListener { _, destination, _ ->
            val dest: String = try {
                resources.getResourceName(destination.id)
            } catch (e: Resources.NotFoundException) {
                Integer.toString(destination.id)
            }

            Toast.makeText(this@MainActivity, "Navigated to $dest",
                Toast.LENGTH_SHORT).show()

            LogWrapper.debug("Navigated to $dest")
        }

        LogWrapper.debug()
    }
}