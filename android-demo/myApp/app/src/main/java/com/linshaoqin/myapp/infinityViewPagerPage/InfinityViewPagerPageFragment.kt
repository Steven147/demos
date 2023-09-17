package com.linshaoqin.myapp.infinityViewPagerPage

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.viewpager2.widget.ViewPager2
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.databinding.InfinityViewPagerPageFragmentBinding

class InfinityViewPagerPageFragment: Fragment() {

    private val viewModel: InfinityViewPagerViewModel by viewModels()
    private val adapter by lazy { InfinityViewPagerPageAdapter()  }


    private lateinit var binding: InfinityViewPagerPageFragmentBinding

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        LogWrapper.debug()
        binding = InfinityViewPagerPageFragmentBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        LogWrapper.debug()
        super.onViewCreated(view, savedInstanceState)
        binding.viewPager.let { viewPager ->
            viewPager.orientation = ViewPager2.ORIENTATION_VERTICAL
            viewPager.adapter = adapter
            // fetch init data
            viewModel.fetchItems()
            // record data
            viewPager.registerOnPageChangeCallback(
                object : ViewPager2.OnPageChangeCallback() {
                    override fun onPageScrollStateChanged(state: Int) {
                        super.onPageScrollStateChanged(state)
                        if (state == ViewPager2.SCROLL_STATE_IDLE) {
                            val lastPosition = viewPager.currentItem
                            if (lastPosition == (adapter.itemCount.minus(1))) {
                                viewModel.fetchItems()
                            }
                        }
                    }
                }
            )
        }

        viewModel.newItemList.observe(viewLifecycleOwner) {
            adapter.addData(it)
        }
        requestInternetPermission()
    }

    private val REQUEST_INTERNET_PERMISSION = 1

    private fun requestInternetPermission() {
        val permissions = arrayOf(
            Manifest.permission.INTERNET
        )
        requestPermissions(permissions, REQUEST_INTERNET_PERMISSION)
    }

    @Deprecated("Deprecated in Java")
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        when (requestCode) {
            REQUEST_INTERNET_PERMISSION -> {
                if ((grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
                    // permission granted
                } else {
                    // permission denied
                }
                return
            }
        }
    }
}