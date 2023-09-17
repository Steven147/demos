package com.linshaoqin.myapp.main

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.databinding.ActivityMainBinding

/**
 * my android demo app
 * see [feishu docs](https://cm0nlh86eu.feishu.cn/wiki/YoHBwLrGFiEu8ckIC8TcEPPSnEd)
 */
class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        LogWrapper.debug()

        supportFragmentManager.beginTransaction().apply {
            replace(binding.mainFragmentContainer.id, MainFragment())
            commit()
        }
    }
}