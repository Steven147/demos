package com.linshaoqin.myapp.main

import androidx.annotation.DrawableRes
import androidx.fragment.app.Fragment
import com.linshaoqin.myapp.R
import com.linshaoqin.myapp.SecondFragment
import com.linshaoqin.myapp.infinityPage.InfinityPageFragment
import com.linshaoqin.myapp.mainPage.MainPageFragment


interface IFragmentItem {

    val fragmentClass: Class<out Fragment>
    val addToBackStack: Boolean
        get() = false
}

interface IListItem {
    val title: String
        get() = ""
    val subtitle: String
        get() = ""

    @get:DrawableRes
    val leftIcon: Int
        get() = R.drawable.ic_arrow_left
    @get:DrawableRes
    val rightIcon: Int
        get() = R.drawable.ic_arrow_right
}
enum class MainFragmentItem : IFragmentItem {
    MAIN_PAGE_FRAGMENT {
        override val fragmentClass = MainPageFragment::class.java
    }
}

enum class MainPageFragmentListItem : IFragmentItem, IListItem {
    INFINITY_PAGE {
        override val fragmentClass = InfinityPageFragment::class.java
        override val title = "infinity page"
        override val subtitle = "page of infinity items"
    },

    SECOND_PAGE {
        override val fragmentClass = SecondFragment::class.java
        override val title = "second page"
        override val subtitle = "page of second"
    };

    companion object {
        fun getList() = listOf(INFINITY_PAGE, SECOND_PAGE)
    }
}