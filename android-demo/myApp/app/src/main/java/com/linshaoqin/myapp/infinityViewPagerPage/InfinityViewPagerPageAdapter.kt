package com.linshaoqin.myapp.infinityViewPagerPage

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.databinding.ViewPagerItemFragmentBinding
import com.linshaoqin.myapp.infinityViewPagerPage.viewPagerItem.ViewPagerItem

class InfinityViewPagerPageAdapter(
    private val dataList: MutableList<ViewPagerItem> = mutableListOf()
//    private var onListEndReached: () -> Unit
) : RecyclerView.Adapter<InfinityViewPagerPageAdapter.MyViewHolder>() {
    class MyViewHolder(
        private val binding: ViewPagerItemFragmentBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(item: ViewPagerItem) {
            binding.titleTextView.text = item.title
            binding.subTitleTextView.text = item.subTitle
            Glide.with(binding.root).load(item.imageUrl).into(binding.imageView)
        }

    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyViewHolder {
        val binding = ViewPagerItemFragmentBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return MyViewHolder(binding)
    }

    override fun onBindViewHolder(holder: MyViewHolder, position: Int) {
        LogWrapper.debug("position $position")
        holder.bind(dataList[position])
//        if (position == dataList.size.minus(1)) {
//            onListEndReached()
//        }
    }

    override fun getItemCount() = dataList.size

    fun addData(newData: List<ViewPagerItem>) {
        LogWrapper.debug()
        val insertIndex = dataList.size
        dataList.addAll(newData)
        // remove loading view in the last (insertIndex), add newData and new loading view
        notifyItemRangeChanged(insertIndex, newData.size)
    }
}