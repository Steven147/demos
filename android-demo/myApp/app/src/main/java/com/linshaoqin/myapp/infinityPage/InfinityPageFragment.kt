package com.linshaoqin.myapp.infinityPage

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.R
import java.util.Random

/**
 * InfinityPageFragment 仅基于fragment和adapter的无限页面
 */
class InfinityPageFragment : Fragment(), InfinityPageAdapter.LoadMoreCallback {
    private lateinit var myAdapter: InfinityPageAdapter
    private var recyclerView: RecyclerView? = null

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.infinity_page_fragment, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        LogWrapper.debug()
        super.onViewCreated(view, savedInstanceState)
        myAdapter = InfinityPageAdapter(mutableListOf("data 1", "data 2", "data 3"), this)
        recyclerView = view.findViewById(R.id.my_recycler_view)
        recyclerView?.apply {
            adapter = myAdapter
            layoutManager = LinearLayoutManager(activity)
        }
    }

    override fun onLoadMore() {
        LogWrapper.debug()
        recyclerView?.postDelayed({
            myAdapter.addData(mutableListOf("data ${Random().nextInt()}"))
        }, 500)
    }
}