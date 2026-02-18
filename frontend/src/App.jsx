import React, { useState } from 'react'
import axios from 'axios'
import { Search, Loader2, Globe, TrendingUp, Shield, BarChart3, Lightbulb } from 'lucide-react'
import { cn } from './lib/utils'

// Placeholder for components we will create
const MacroCard = ({ data }) => (
  <div className="bg-white p-6 rounded-xl border border-google-border shadow-sm">
    <div className="flex items-center gap-2 mb-4 text-google-blue">
      <TrendingUp size={20} />
      <h3 className="font-semibold text-lg text-gray-800">Macro Economics</h3>
    </div>
    <div className="grid grid-cols-2 gap-4">
      {Object.entries(data || {}).map(([key, value]) => (
        <div key={key} className="p-3 bg-gray-50 rounded-lg">
          <p className="text-xs text-gray-500 uppercase font-medium">
            {key === 'gdp' ? 'GDP (current US$)' : key.replace('_', ' ')}
          </p>
          <p className="text-lg font-bold text-gray-800">
            {value && value[0] ? (
              key === 'gdp' && typeof value[0].value === 'number'
                ? (value[0].value >= 1e12
                  ? `${(value[0].value / 1e12).toFixed(2)} T`
                  : `${(value[0].value / 1e9).toFixed(2)} B`)
                : (typeof value[0].value === 'number' ? value[0].value.toLocaleString() : value[0].value)
            ) : 'N/A'}
          </p>
        </div>
      ))}
    </div>
  </div>
)

const FDICard = ({ data }) => (
  <div className="bg-white p-6 rounded-xl border border-google-border shadow-sm">
    <div className="flex items-center gap-2 mb-4 text-google-green">
      <BarChart3 size={20} />
      <h3 className="font-semibold text-lg text-gray-800">FDI Overview</h3>
    </div>
    <div className="space-y-4">
      {data?.map((item, idx) => (
        <div key={idx} className="border-b border-gray-100 pb-3 last:border-0">
          <p className="text-sm font-semibold text-gray-700">{item.indicator}</p>
          <div className="flex gap-4 mt-2 overflow-x-auto pb-2">
            {item.values.map((v, i) => (
              <div key={i} className="text-center min-w-[60px]">
                <p className="text-[10px] text-gray-400">{v.year}</p>
                <p className="text-xs font-medium text-gray-600">{(v.value / 1e9).toFixed(1)}B</p>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  </div>
)

const PoliticalCard = ({ wiki, political, aiPolitical }) => {
  const categories = aiPolitical || {};

  return (
    <div className="bg-white p-6 rounded-xl border border-google-border shadow-sm">
      <div className="flex items-center gap-2 mb-4 text-google-red">
        <Shield size={20} />
        <h3 className="font-semibold text-lg text-gray-800">Political Landscape</h3>
      </div>
      <div className="prose prose-sm max-w-none text-gray-600">
        <p className="mb-4">{wiki?.extract}</p>

        {aiPolitical ? (
          <div className="space-y-4 pt-2">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-red-50 p-3 rounded-lg">
                <p className="text-[10px] text-gray-500 uppercase font-bold">Government</p>
                <p className="text-sm font-medium text-gray-800">{categories.government_type}</p>
              </div>
              <div className="bg-red-50 p-3 rounded-lg">
                <p className="text-[10px] text-gray-500 uppercase font-bold">Stability</p>
                <p className="text-sm font-medium text-gray-800">{categories.stability}</p>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-[10px] text-gray-500 uppercase font-bold">Current Leaders</p>
              <div className="flex flex-wrap gap-1">
                {categories.current_leaders?.map((l, i) => (
                  <span key={i} className="px-2 py-0.5 bg-gray-100 rounded text-xs">{l}</span>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-[10px] text-gray-500 uppercase font-bold">Major Parties</p>
              <div className="flex flex-wrap gap-1">
                {categories.major_parties?.map((p, i) => (
                  <span key={i} className="px-2 py-0.5 bg-gray-100 rounded text-xs">{p}</span>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-[10px] text-gray-500 uppercase font-bold">Upcoming Elections</p>
                <p className="text-xs text-gray-700">{categories.upcoming_elections}</p>
              </div>
              <div>
                <p className="text-[10px] text-gray-500 uppercase font-bold">Recent Conflicts</p>
                <p className="text-xs text-gray-700">{categories.recent_conflicts}</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-4">
            {Object.entries(political || {}).map(([key, value]) => (
              <div key={key} className="flex justify-between border-b border-gray-50 py-1">
                <span className="text-xs font-semibold text-gray-500">{key}:</span>
                <span className="text-xs text-gray-700 text-right">{value}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const InsightCard = ({ insights }) => {
  const renderValue = (val) => {
    if (typeof val === 'string') return val;
    if (typeof val === 'object' && val !== null) {
      return (
        <div className="space-y-1 mt-1">
          {Object.entries(val).map(([k, v]) => (
            <div key={k} className="text-xs">
              <span className="font-semibold text-gray-600 uppercase text-[10px]">{k.replace(/_/g, ' ')}:</span>
              <span className="ml-1">{Array.isArray(v) ? v.join(', ') : String(v)}</span>
            </div>
          ))}
        </div>
      );
    }
    return String(val || '');
  };

  return (
    <div className="bg-blue-50 p-6 rounded-xl border border-blue-100 shadow-sm">
      <div className="flex items-center gap-2 mb-4 text-google-blue">
        <Lightbulb size={20} />
        <h3 className="font-semibold text-lg text-gray-800">AI Insights</h3>
      </div>
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-bold text-blue-800 mb-1">Investment Climate</h4>
          <div className="text-sm text-gray-700">{renderValue(insights?.investment_climate_summary)}</div>
        </div>
        <div>
          <h4 className="text-sm font-bold text-blue-800 mb-1">Political Overview</h4>
          <div className="text-sm text-gray-700">{renderValue(insights?.political_summary)}</div>
        </div>
        <div className="bg-white p-3 rounded-lg border border-blue-200">
          <h4 className="text-sm font-bold text-gray-700 mb-2">Key Takeaways</h4>
          <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
            {insights?.key_takeaways?.map((item, i) => <li key={i}>{typeof item === 'object' ? JSON.stringify(item) : item}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query) return
    setLoading(true)
    setError(null)
    try {
      const resp = await axios.get(`http://localhost:8000/api/country/${query}`)
      setData(resp.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch country data')
    } finally {
      setLoading(false)
    }
  }

  const goHome = () => {
    setData(null)
    setQuery('')
    setError(null)
  }

  return (
    <div className="min-h-screen bg-google-gray text-gray-900 font-sans">
      {/* Header */}
      <nav className="bg-white border-b border-google-border sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div
              className="flex items-center gap-2 cursor-pointer group"
              onClick={goHome}
            >
              <div className="bg-google-blue p-2 rounded-lg group-hover:bg-blue-600 transition-colors">
                <Globe className="text-white" size={24} />
              </div>
              <span className="text-xl font-bold text-gray-700 tracking-tight group-hover:text-google-blue transition-colors">CountryProfile</span>
            </div>

            <form onSubmit={handleSearch} className="flex-1 max-w-lg mx-8">
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search className="text-gray-400 group-focus-within:text-google-blue transition-colors" size={18} />
                </div>
                <input
                  type="text"
                  className="block w-full pl-10 pr-3 py-2 border border-google-border rounded-full leading-5 bg-gray-50 placeholder-gray-500 focus:outline-none focus:bg-white focus:ring-1 focus:ring-google-blue focus:border-google-blue sm:text-sm transition-all shadow-sm"
                  placeholder="Search countries (e.g. UAE, United Kingdom...)"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
              </div>
            </form>

            <div className="hidden md:flex items-center gap-4">
              <div className="w-8 h-8 rounded-full bg-google-yellow flex items-center justify-center text-white font-bold">U</div>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!data && !loading && !error && (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="bg-white p-8 rounded-2xl border border-google-border shadow-md max-w-md">
              <Globe size={64} className="text-google-blue mx-auto mb-4 animate-pulse" />
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Global Economic Insight</h2>
              <p className="text-gray-500 mb-6">Enter a country name or ISO code above to view macroeconomic data, investment climate, and political landscape.</p>
              <div className="flex flex-wrap gap-2 justify-center">
                {['UAE', 'USA', 'IND', 'GBR'].map(c => (
                  <button key={c} onClick={() => { setQuery(c); }} className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-xs font-medium text-gray-600 transition-colors">{c}</button>
                ))}
              </div>
            </div>
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader2 className="text-google-blue animate-spin mb-4" size={48} />
            <p className="text-gray-500 font-medium">Fetching global insights...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-100 p-4 rounded-xl text-red-700 mb-8 max-w-2xl mx-auto flex items-center gap-3">
            <div className="bg-red-100 p-2 rounded-lg text-red-600">!</div>
            <p>{error}</p>
          </div>
        )}

        {data && !loading && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center gap-4 mb-8">
              <img src={data.metadata.flag} alt="Flag" className="h-10 w-auto shadow-sm border border-gray-100 rounded-sm" />
              <div>
                <h1 className="text-3xl font-bold text-gray-800 tracking-tight">{data.metadata.name}</h1>
                <p className="text-sm text-gray-500 font-medium">{data.metadata.code} • Regional Economic Profile</p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-6">
                <InsightCard insights={data.insights.raw ? null : data.insights} />
                <MacroCard data={data.macro} />
                <FDICard data={data.fdi} />
              </div>
              <div className="space-y-6">
                <PoliticalCard
                  wiki={data.wiki}
                  political={data.political}
                  aiPolitical={data.insights?.political_landscape}
                />
                <div className="bg-white p-6 rounded-xl border border-google-border shadow-sm">
                  <h4 className="font-semibold text-gray-800 mb-3">Data Sources</h4>
                  <ul className="space-y-2">
                    {['UNCTAD', 'World Bank', 'Wikipedia'].map(s => (
                      <li key={s} className="flex items-center gap-2 text-xs text-gray-500">
                        <div className="w-1 h-1 rounded-full bg-google-blue"></div>
                        <span>Primary data from {s}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
