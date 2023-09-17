package com.linshaoqin.myapp.infinityViewPagerPage

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.linshaoqin.myapp.infinityViewPagerPage.viewPagerItem.ViewPagerItem
import kotlinx.coroutines.launch

class InfinityViewPagerViewModel : ViewModel() {

    private val _newItemList = MutableLiveData<MutableList<ViewPagerItem>>()
    val newItemList: LiveData<MutableList<ViewPagerItem>> get() = _newItemList

    fun fetchItems() {
        viewModelScope.launch {
            _newItemList.value = ItemApi.getItemList(3)
        }
    }
}