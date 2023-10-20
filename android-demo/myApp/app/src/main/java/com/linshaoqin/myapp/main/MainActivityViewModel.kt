package com.linshaoqin.myapp.main

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.navigation.NavController
import com.linshaoqin.myapp.LogWrapper

class MainActivityViewModel : ViewModel() {
    // live data post live value and state
    private val _selectedPosition = MutableLiveData<Int>()
    val selectedPosition: LiveData<Int> get() = _selectedPosition

    private val _currentFragment = MutableLiveData<IFragmentItem>()
    val currentFragment: LiveData<IFragmentItem> get() = _currentFragment
    fun updateSelectedPosition(position: Int) {
        _selectedPosition.value = position
    }

    private fun updateFragment(item: IFragmentItem) {
        _currentFragment.value = item
        LogWrapper.debug()
    }

    fun updatePage(navController: NavController, item: IFragmentItem) {
        navController.navigate(item.startAction)
        updateFragment(item)
    }
}
