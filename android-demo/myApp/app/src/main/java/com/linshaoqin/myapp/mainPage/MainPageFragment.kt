package com.linshaoqin.myapp.mainPage

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.SecondFragment
import com.linshaoqin.myapp.databinding.MainPageFragmentBinding
import com.linshaoqin.myapp.main.MainFragmentViewModel

class MainPageFragment : Fragment() {
    private lateinit var binding: MainPageFragmentBinding
    private var recyclerView: RecyclerView? = null
    private val mainPageVM: MainPageViewModel by lazy {
        ViewModelProvider(this).get(MainPageViewModel::class.java)
    }
    private val mainFragmentVM: MainFragmentViewModel by activityViewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = MainPageFragmentBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val adapter = MainPageAdapter(mainPageVM, mainFragmentVM)
        recyclerView = binding.recyclerView
        recyclerView?.adapter = adapter
        recyclerView?.layoutManager = LinearLayoutManager(requireContext())

        mainPageVM.dataList.observe(viewLifecycleOwner, Observer {
            adapter.notifyDataSetChanged()
        })

        LogWrapper.debug()
    }
}