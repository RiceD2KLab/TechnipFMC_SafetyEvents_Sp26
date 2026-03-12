import { useState, useMemo } from "react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "../ui/popover";
import {
  Command,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
} from "../ui/command";
import { ChevronsUpDown } from "lucide-react";
import type { IncidentOption } from "../../types/kg";

interface KgComboboxProps {
  incidents: IncidentOption[];
  value: string | null;
  onSelect: (entityId: string) => void;
  loading?: boolean;
}

export default function KgCombobox({
  incidents,
  value,
  onSelect,
  loading,
}: KgComboboxProps) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");

  const filtered = useMemo(() => {
    if (!search.trim()) return incidents.slice(0, 100);
    const lower = search.toLowerCase();
    return incidents
      .filter((i) => i.label.toLowerCase().includes(lower))
      .slice(0, 100);
  }, [incidents, search]);

  const selectedLabel = useMemo(() => {
    if (!value) return null;
    return incidents.find((i) => i.entity_id === value)?.label ?? value;
  }, [incidents, value]);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <button
          className="flex w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-left hover:bg-gray-50"
          disabled={loading}
        >
          <span className="truncate text-gray-700">
            {loading
              ? "Loading incidents..."
              : selectedLabel
                ? selectedLabel
                : "Select an incident..."}
          </span>
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 text-gray-400" />
        </button>
      </PopoverTrigger>
      <PopoverContent className="w-[400px] p-0" align="start">
        <Command shouldFilter={false}>
          <CommandInput
            placeholder="Type to search incidents..."
            value={search}
            onValueChange={setSearch}
          />
          <CommandList>
            <CommandEmpty>No incidents found.</CommandEmpty>
            <CommandGroup>
              {filtered.map((incident) => (
                <CommandItem
                  key={incident.entity_id}
                  value={incident.entity_id}
                  onSelect={() => {
                    onSelect(incident.entity_id);
                    setOpen(false);
                    setSearch("");
                  }}
                >
                  <span className="truncate text-xs">{incident.label}</span>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
