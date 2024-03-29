package com.linshaoqin.myapp.mainPage

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.navigation.findNavController
import androidx.recyclerview.widget.RecyclerView
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.R
import com.linshaoqin.myapp.main.MainActivityViewModel

class MainPageAdapter(
    private val mainPageVM: MainPageViewModel,
    private val mainActivityVM: MainActivityViewModel
) : RecyclerView.Adapter<MainPageAdapter.ViewHolder>() {

    init {
        LogWrapper.debug()
    }

    /**
     * Provide a reference to the type of views that you are using
     * (custom ViewHolder)
     */
    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val title: TextView
        val subtitle: TextView
        val leftIcon: ImageView
        val rightIcon: ImageView

        init {
            // Define click listener for the ViewHolder's View
            title = view.findViewById(R.id.item_title)
            subtitle = view.findViewById(R.id.item_subtitle)
            leftIcon = view.findViewById(R.id.item_left_icon)
            rightIcon = view.findViewById(R.id.item_right_icon)
        }
    }

    // Create new views (invoked by the layout manager)
    override fun onCreateViewHolder(viewGroup: ViewGroup, viewType: Int): ViewHolder {
        LogWrapper.debug()
        // Create a new view, which defines the UI of the list item
        val view = LayoutInflater.from(viewGroup.context)
            .inflate(R.layout.main_page_fragment_list_item, viewGroup, false)

        return ViewHolder(view)
    }

    // Replace the contents of a view (invoked by the layout manager)
    override fun onBindViewHolder(viewHolder: ViewHolder, position: Int) {

        // Get element from your dataset at this position and replace the
        // contents of the view with that element
        val item = mainPageVM.dataList.value?.get(position) ?: return
        viewHolder.title.text = item.title
        viewHolder.subtitle.text = item.subtitle
        viewHolder.leftIcon.setImageResource(item.leftIcon)
        viewHolder.rightIcon.setImageResource(item.rightIcon)
        viewHolder.itemView.let { itemView ->
            itemView.setOnClickListener {
                mainActivityVM.updatePage(itemView.findNavController(), item)
            }
        }
    }

    // Return the size of your dataset (invoked by the layout manager)
    override fun getItemCount() = mainPageVM.dataList.value?.size ?: 0
}