package com.linshaoqin.myapp.main

import androidx.annotation.DrawableRes
import androidx.annotation.IdRes
import com.linshaoqin.myapp.R

interface IFragmentItem {
    @get:IdRes
    val startAction: Int
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

enum class MainPageFragmentListItem : IFragmentItem, IListItem {
    INFINITY_PAGE {
        override val startAction = R.id.action_MainPageFragment_to_infinityPageFragment
        override val title = "infinity page"
        override val subtitle = "page of infinity items"
    },

    INFINITY_VP_PAGE {
        override val startAction = R.id.action_MainPageFragment_to_infinityViewPagerPageFragment
        override val title = "infinity viewpager page"
        override val subtitle = "page of infinity viewpager"
    },

    SECOND_PAGE {
        override val startAction = R.id.action_MainPageFragment_to_SecondFragment2
        override val title = "second page"
        override val subtitle = "page of second"
    };

    companion object {
        fun getList() = listOf(INFINITY_VP_PAGE, INFINITY_PAGE, SECOND_PAGE)
    }
}