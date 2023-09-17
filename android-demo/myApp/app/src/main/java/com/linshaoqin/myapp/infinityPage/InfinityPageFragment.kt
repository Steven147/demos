package com.linshaoqin.myapp.infinityPage

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.ViewTreeObserver
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.R
import com.linshaoqin.myapp.databinding.FragmentSecondBinding
import com.linshaoqin.myapp.databinding.InfinityPageFragmentBinding
import com.linshaoqin.myapp.main.MainFragmentItem
import com.linshaoqin.myapp.main.MainFragmentViewModel


class InfinityPageFragment : Fragment(), InfinityPageAdapter.LoadMoreCallback {
    private lateinit var myAdapter: InfinityPageAdapter
    private lateinit var binding: InfinityPageFragmentBinding
    private val mainFragmentVM: MainFragmentViewModel by activityViewModels()

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        binding = InfinityPageFragmentBinding.inflate(inflater, container, false)
        myAdapter = InfinityPageAdapter(mutableListOf("data 1", "data 2", "data 3"), this)
        binding.myRecyclerView.adapter = myAdapter
        binding.myRecyclerView.layoutManager = LinearLayoutManager(activity)
        return binding.root
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        LogWrapper.debug()
        binding.buttonSecond.setOnClickListener {
            mainFragmentVM.updateFragment(MainFragmentItem.MAIN_PAGE_FRAGMENT)
        }
    }

    override fun onLoadMore() {
        LogWrapper.debug()
        binding.myRecyclerView.postDelayed({
            myAdapter.addData(mutableListOf("data 4"))
        }, 500)
    }
}