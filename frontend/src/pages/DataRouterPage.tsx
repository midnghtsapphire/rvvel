import { useState } from 'react'
import { GitBranch, Plus, Play, Pause, Trash2, Mail, FolderOpen, Github } from 'lucide-react'

interface RoutingRule {
  id: string
  name: string
  sourceType: string
  sourcePattern: string
  destinationType: string
  destinationPath: string
  isActive: boolean
  triggerCount: number
}

const mockRules: RoutingRule[] = [
  {
    id: '1', name: 'Invoices to Accounting', sourceType: 'Gmail', sourcePattern: 'invoice|receipt|payment',
    destinationType: 'Google Drive', destinationPath: '/Accounting/Invoices', isActive: true, triggerCount: 47,
  },
  {
    id: '2', name: 'GitHub Issues to Tracker', sourceType: 'GitHub', sourcePattern: 'bug|feature|enhancement',
    destinationType: 'Google Drive', destinationPath: '/Dev/Issues', isActive: true, triggerCount: 23,
  },
  {
    id: '3', name: 'Client Emails to CRM', sourceType: 'Gmail', sourcePattern: 'from:.*@client\\.com',
    destinationType: 'Google Drive', destinationPath: '/CRM/Clients', isActive: false, triggerCount: 12,
  },
]

const sourceIcons: Record<string, typeof Mail> = {
  Gmail: Mail,
  'Google Drive': FolderOpen,
  GitHub: Github,
}

export default function DataRouterPage() {
  const [rules, setRules] = useState(mockRules)

  const toggleRule = (id: string) => {
    setRules(prev => prev.map(r => r.id === id ? { ...r, isActive: !r.isActive } : r))
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold gradient-text mb-2">Universal Data Router</h1>
          <p className="text-secondary-brand text-sm">
            Automatically route emails, files, and data between Gmail, Google Drive, and GitHub.
          </p>
        </div>
        <button className="glass-btn-primary flex items-center gap-2" aria-label="Create new routing rule">
          <Plus className="w-4 h-4" aria-hidden="true" />
          New Rule
        </button>
      </div>

      {/* Rules list */}
      <div className="space-y-3" role="list" aria-label="Routing rules">
        {rules.map((rule) => {
          const SourceIcon = sourceIcons[rule.sourceType] || GitBranch
          return (
            <div
              key={rule.id}
              role="listitem"
              className={`glass-card flex items-center gap-4 ${!rule.isActive ? 'opacity-60' : ''}`}
            >
              <div className="p-2 rounded-lg bg-dark-glass" aria-hidden="true">
                <SourceIcon className="w-5 h-5 text-primary" />
              </div>

              <div className="flex-1 min-w-0">
                <h3 className="font-medium text-sm">{rule.name}</h3>
                <p className="text-xs text-secondary-brand truncate">
                  {rule.sourceType}: <code className="text-primary">{rule.sourcePattern}</code>
                  {' → '}{rule.destinationType}: {rule.destinationPath}
                </p>
              </div>

              <div className="text-right text-xs text-secondary-brand" aria-label={`Triggered ${rule.triggerCount} times`}>
                <span className="text-primary font-semibold">{rule.triggerCount}</span> triggers
              </div>

              <div className="flex items-center gap-1">
                <button
                  onClick={() => toggleRule(rule.id)}
                  className="glass-btn p-2"
                  aria-label={rule.isActive ? `Pause rule: ${rule.name}` : `Activate rule: ${rule.name}`}
                >
                  {rule.isActive ? (
                    <Pause className="w-4 h-4" aria-hidden="true" />
                  ) : (
                    <Play className="w-4 h-4" aria-hidden="true" />
                  )}
                </button>
                <button className="glass-btn p-2 hover:text-red-400" aria-label={`Delete rule: ${rule.name}`}>
                  <Trash2 className="w-4 h-4" aria-hidden="true" />
                </button>
              </div>
            </div>
          )
        })}
      </div>

      {/* Empty state */}
      {rules.length === 0 && (
        <div className="glass-card text-center py-12">
          <GitBranch className="w-12 h-12 text-secondary-brand mx-auto mb-4" aria-hidden="true" />
          <h2 className="text-lg font-semibold mb-2">No Routing Rules Yet</h2>
          <p className="text-secondary-brand text-sm mb-4">
            Create your first rule to automatically route data between your services.
          </p>
          <button className="glass-btn-primary" aria-label="Create your first routing rule">
            <Plus className="w-4 h-4 inline mr-1" aria-hidden="true" />
            Create First Rule
          </button>
        </div>
      )}
    </div>
  )
}
