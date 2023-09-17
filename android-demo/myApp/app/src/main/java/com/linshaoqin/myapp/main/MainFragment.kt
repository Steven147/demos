package com.linshaoqin.myapp.main

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentTransaction
import androidx.fragment.app.activityViewModels
import androidx.lifecycle.Observer
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.databinding.MainFragmentBinding

class MainFragment : Fragment() {
    private lateinit var binding: MainFragmentBinding
    private val mainFragmentVM: MainFragmentViewModel by activityViewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = MainFragmentBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        LogWrapper.debug()

        mainFragmentVM.currentFragment.observe(viewLifecycleOwner, Observer {
            val newFragment = it.fragmentClass.newInstance()
            val addToBackStack = it.addToBackStack
            switchToInnerFragment(newFragment, addToBackStack) {}
        })

        mainFragmentVM.updateFragment(MainFragmentItem.MAIN_PAGE_FRAGMENT)
    }

    private fun switchToInnerFragment(
        fragment: Fragment,
        addToBackStack: Boolean = false,
        transition: FragmentTransaction.() -> Unit
    ) {
        LogWrapper.debug()
        childFragmentManager.beginTransaction().apply {
            setCustomAnimations(android.R.anim.fade_in, android.R.anim.fade_out)
            transition()
            if (addToBackStack) {
                add(binding.fragmentContainer.id, fragment, "inner_tag")
                addToBackStack("inner_tag")
            } else {
                replace(binding.fragmentContainer.id, fragment, "inner_tag")
            }
            commit()
        }
    }
}