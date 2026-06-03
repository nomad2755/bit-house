import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useLocationStore = defineStore('location', () => {
  const provinces = ref<any[]>([])
  const selectedProvince = ref<number | undefined>(
    Number(localStorage.getItem('province_id')) || undefined
  )
  const selectedCity = ref<number | undefined>(
    Number(localStorage.getItem('city_id')) || undefined
  )
  const cityName = ref(localStorage.getItem('city_name') || '')

  const currentCities = computed(() => {
    const p = provinces.value.find((x: any) => x.id === selectedProvince.value)
    return p ? p.cities : []
  })

  async function loadProvinces() {
    if (provinces.value.length) return
    const res = await api.get('/houses/provinces/')
    provinces.value = res.data
    // 默认选择第一个省份城市
    if (!selectedProvince.value && res.data.length) {
      const firstProvince = res.data[0]
      if (firstProvince.cities?.length) {
        selectCity(firstProvince.id, firstProvince.cities[0].id, firstProvince.cities[0].name)
      }
    }
  }

  function selectCity(provinceId: number, cityId: number, name: string) {
    selectedProvince.value = provinceId
    selectedCity.value = cityId
    cityName.value = name
    localStorage.setItem('province_id', String(provinceId))
    localStorage.setItem('city_id', String(cityId))
    localStorage.setItem('city_name', name)
  }

  function clearCity() {
    selectedProvince.value = undefined
    selectedCity.value = undefined
    cityName.value = ''
    localStorage.removeItem('province_id')
    localStorage.removeItem('city_id')
    localStorage.removeItem('city_name')
  }

  return {
    provinces, selectedProvince, selectedCity, cityName, currentCities,
    loadProvinces, selectCity, clearCity,
  }
})
