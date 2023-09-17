package com.linshaoqin.myapp.mainPage

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.linshaoqin.myapp.main.MainPageFragmentListItem

class MainPageViewModel : ViewModel() {
    private val _dataList = MutableLiveData<List<MainPageFragmentListItem>>()
    val dataList: LiveData<List<MainPageFragmentListItem>> get() = _dataList

    init {
        initDataList()
    }

    private fun initDataList() {
        val list = mutableListOf<MainPageFragmentListItem>()
        list.addAll(MainPageFragmentListItem.getList())

        _dataList.value = list
    }
}