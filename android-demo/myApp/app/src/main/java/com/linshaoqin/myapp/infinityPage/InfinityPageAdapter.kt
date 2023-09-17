package com.linshaoqin.myapp.infinityPage

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.R

class InfinityPageAdapter(
    private val dataList: MutableList<String>,
    private val loadMoreCallback: LoadMoreCallback
)
    : RecyclerView.Adapter<InfinityPageAdapter.InfinityPageViewHolder>() {


    class InfinityPageViewHolder(private val itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val myTextView: TextView = itemView.findViewById(R.id.my_text_view)

        fun bind(data: String) {
            myTextView.text = data
            // 添加其他操作
        }
    }
    interface LoadMoreCallback {
        fun onLoadMore()
    }

    private val ITEM_VIEW_TYPE_DATA = 1
    private val ITEM_VIEW_TYPE_LOADING = 2

    override fun getItemCount(): Int {
        return dataList.size + 1
    }

    override fun getItemViewType(position: Int): Int {
        return if (position < dataList.size) ITEM_VIEW_TYPE_DATA else ITEM_VIEW_TYPE_LOADING
    }

    override fun onBindViewHolder(holder: InfinityPageViewHolder, position: Int) {
        LogWrapper.debug("position $position")
        if (getItemViewType(position) == ITEM_VIEW_TYPE_DATA) {
            val data = dataList[position]
            holder.bind(data)
        } else {
            loadMoreCallback.onLoadMore()
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): InfinityPageViewHolder {
        LogWrapper.debug()
        return if (viewType == ITEM_VIEW_TYPE_DATA) {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.infinity_page_fragment_list_item, parent, false)
            InfinityPageViewHolder(view)
        } else {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.infinity_page_fragment_list_loading_item, parent, false)
            InfinityPageViewHolder(view)
        }
    }

    fun addData(newData: List<String>) {
        LogWrapper.debug()
        val insertIndex = dataList.size
        dataList.addAll(newData)
        // remove loading view in the last (insertIndex), add newData and new loading view
        notifyItemRangeChanged(insertIndex, newData.size + 1)
    }
}

