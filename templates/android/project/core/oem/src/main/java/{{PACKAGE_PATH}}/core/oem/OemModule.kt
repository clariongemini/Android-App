package {{PACKAGE}}.core.oem

import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class OemModule {

    @Binds
    @Singleton
    abstract fun bindManufacturerDetector(impl: DefaultManufacturerDetector): ManufacturerDetector

    @Binds
    @Singleton
    abstract fun bindOemBatteryOptimizer(impl: DefaultOemBatteryOptimizer): OemBatteryOptimizer

    @Binds
    @Singleton
    abstract fun bindOemAutostartGuide(impl: DefaultOemAutostartGuide): OemAutostartGuide

    @Binds
    @Singleton
    abstract fun bindOemCompatFacade(impl: DefaultOemCompatFacade): OemCompatFacade
}
