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
import com.linshaoqin.myapp.R
import com.linshaoqin.myapp.main.MainActivityViewModel

class MainPageFragment : Fragment() {
    private var recyclerView: RecyclerView? = null
    private val mainPageVM: MainPageViewModel by lazy {
        ViewModelProvider(this).get(MainPageViewModel::class.java)
    }
    private val mainActivityVM: MainActivityViewModel by activityViewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        return inflater.inflate(R.layout.main_page_fragment, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        recyclerView = view.findViewById(R.id.recycler_view)
        recyclerView?.adapter = MainPageAdapter(mainPageVM, mainActivityVM)
        recyclerView?.layoutManager = LinearLayoutManager(requireContext())

        mainPageVM.dataList.observe(viewLifecycleOwner, Observer {
            recyclerView?.adapter?.notifyDataSetChanged()
        })

        LogWrapper.debug()
    }
}