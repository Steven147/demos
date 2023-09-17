package com.linshaoqin.myapp.main

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.linshaoqin.myapp.LogWrapper

class MainFragmentViewModel : ViewModel() {
    // live data post live value and state
    private val _selectedPosition = MutableLiveData<Int>()
    val selectedPosition: LiveData<Int> get() = _selectedPosition

    private val _currentFragment = MutableLiveData<IFragmentItem>()
    val currentFragment: LiveData<IFragmentItem> get() = _currentFragment
    fun updateSelectedPosition(position: Int) {
        _selectedPosition.value = position
    }

    fun updateFragment(item: IFragmentItem) {
        _currentFragment.value = item
        LogWrapper.debug()
    }
}
