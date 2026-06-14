package {{PACKAGE}}.feature.premium.data

import android.app.Activity
import android.content.Context
import com.android.billingclient.api.BillingClient
import com.android.billingclient.api.BillingClientStateListener
import com.android.billingclient.api.BillingFlowParams
import com.android.billingclient.api.BillingResult
import com.android.billingclient.api.ProductDetails
import com.android.billingclient.api.Purchase
import com.android.billingclient.api.PurchasesUpdatedListener
import com.android.billingclient.api.QueryProductDetailsParams
import {{PACKAGE}}.core.common.result.AppResult
import {{PACKAGE}}.feature.premium.domain.SubscriptionState
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Google Play Billing — 7 gün trial + abonelik.
 * @see docs/03-STANDARDS/MONETIZATION_TECH.md
 */
@Singleton
class BillingRepository @Inject constructor(
    @ApplicationContext private val context: Context,
) : PurchasesUpdatedListener {

    private val _state = MutableStateFlow<SubscriptionState>(SubscriptionState.Free)
    val state: StateFlow<SubscriptionState> = _state

    private val billingClient: BillingClient = BillingClient.newBuilder(context)
        .setListener(this)
        .enablePendingPurchases()
        .build()

    fun startConnection(onReady: () -> Unit) {
        billingClient.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(result: BillingResult) {
                if (result.responseCode == BillingClient.BillingResponseCode.OK) onReady()
            }

            override fun onBillingServiceDisconnected() {
                billingClient.startConnection(this)
            }
        })
    }

    fun launchTrialSubscription(activity: Activity, productDetails: ProductDetails): AppResult<Unit> {
        val offer = productDetails.subscriptionOfferDetails?.firstOrNull()
            ?: return AppResult.Error("No offer")
        val params = BillingFlowParams.newBuilder()
            .setProductDetailsParamsList(
                listOf(
                    BillingFlowParams.ProductDetailsParams.newBuilder()
                        .setProductDetails(productDetails)
                        .setOfferToken(offer.offerToken)
                        .build(),
                ),
            ).build()
        val result = billingClient.launchBillingFlow(activity, params)
        return if (result.responseCode == BillingClient.BillingResponseCode.OK) {
            AppResult.Success(Unit)
        } else {
            AppResult.Error("Billing flow failed: ${result.debugMessage}")
        }
    }

    override fun onPurchasesUpdated(result: BillingResult, purchases: MutableList<Purchase>?) {
        if (result.responseCode != BillingClient.BillingResponseCode.OK || purchases.isNullOrEmpty()) {
            return
        }
        val active = purchases.any { it.purchaseState == Purchase.PurchaseState.PURCHASED }
        _state.value = if (active) {
            SubscriptionState.Active(planId = purchases.first().products.firstOrNull() ?: "premium")
        } else {
            SubscriptionState.Free
        }
    }

    fun queryProducts(productIds: List<String>, onResult: (List<ProductDetails>) -> Unit) {
        val params = QueryProductDetailsParams.newBuilder()
            .setProductList(
                productIds.map {
                    QueryProductDetailsParams.Product.newBuilder()
                        .setProductId(it)
                        .setProductType(BillingClient.ProductType.SUBS)
                        .build()
                },
            ).build()
        billingClient.queryProductDetailsAsync(params) { _, list -> onResult(list) }
    }
}
