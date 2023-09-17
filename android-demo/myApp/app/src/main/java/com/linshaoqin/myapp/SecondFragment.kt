package com.linshaoqin.myapp

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import com.linshaoqin.myapp.databinding.FragmentSecondBinding
import com.linshaoqin.myapp.main.MainFragmentItem
import com.linshaoqin.myapp.main.MainFragmentViewModel

/**
 * A simple [Fragment] subclass as the second destination in the navigation.
 */
class SecondFragment : Fragment() {

    private val mainFragmentVM: MainFragmentViewModel by activityViewModels()
    private var _binding: FragmentSecondBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentSecondBinding.inflate(inflater, container, false)
        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding.buttonSecond.setOnClickListener {
            mainFragmentVM.updateFragment(MainFragmentItem.MAIN_PAGE_FRAGMENT)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}