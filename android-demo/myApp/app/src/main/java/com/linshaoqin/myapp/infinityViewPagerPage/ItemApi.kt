package com.linshaoqin.myapp.infinityViewPagerPage

import com.google.gson.Gson
import com.google.gson.JsonObject
import com.linshaoqin.myapp.LogWrapper
import com.linshaoqin.myapp.infinityViewPagerPage.viewPagerItem.ViewPagerItem
import okhttp3.ResponseBody
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path

object ItemApi {
    const val baseUrl = "http://casaos.local:5000"
    suspend fun getItemList(size: Int): MutableList<ViewPagerItem> {

        val viewPagerItemList = mutableListOf<ViewPagerItem>()
        val apiService = Retrofit.Builder()
            .baseUrl(baseUrl)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)

        val responseBody = apiService.getImages(size)
        try {
            // todo catch error
            val responseJson = responseBody.string()
            val jsonObject = Gson().fromJson(responseJson, JsonObject::class.java)
            LogWrapper.debug(jsonObject.toString())
            val imageUrlsJsonArray = jsonObject.getAsJsonArray("image_urls")
            for (i in 0 until imageUrlsJsonArray.size()) {
                val url = imageUrlsJsonArray[i].asString
                val viewPagerItem = ViewPagerItem(i, "Title", "Subtitle", baseUrl+url)
                viewPagerItemList.add(viewPagerItem)
            }
            return viewPagerItemList
        } catch (t: Throwable) {
            LogWrapper.debug(t.toString())
        }

        return viewPagerItemList
    }
}

interface ApiService {
    @GET("/images/{count}")
    suspend fun getImages(@Path("count") id: Int): ResponseBody
}