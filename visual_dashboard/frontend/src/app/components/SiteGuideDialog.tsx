import { HelpCircle } from "lucide-react";
import { Button } from "./ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./ui/dialog";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "./ui/accordion";

export default function SiteGuideDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button
          type="button"
          variant="default"
          size="lg"
          className="h-12 min-h-12 border-0 bg-blue-600 px-6 text-base font-bold text-white shadow-lg shadow-blue-600/40 ring-2 ring-white ring-offset-2 ring-offset-white hover:bg-blue-700 hover:shadow-xl hover:shadow-blue-600/45 focus-visible:ring-4 focus-visible:ring-blue-400/70"
        >
          <HelpCircle className="size-6 shrink-0 stroke-[2.5]" aria-hidden />
          How to use this site
        </Button>
      </DialogTrigger>
      <DialogContent className="max-h-[min(85vh,760px)] gap-0 overflow-y-auto p-0 sm:max-w-2xl">
        <DialogHeader className="space-y-2 border-b border-gray-100 px-6 pt-6 pb-4 pr-14 text-left">
          <DialogTitle className="text-xl font-semibold text-gray-900">
            How to use this site
          </DialogTitle>
          <DialogDescription className="text-base leading-relaxed text-gray-600">
            Quick tips for the Safety Analytics Platform. Open any section below
            for step-by-step help.
          </DialogDescription>
        </DialogHeader>

        <div className="px-6 py-4">
          <Accordion
            type="single"
            collapsible
            defaultValue="overview"
            className="w-full"
          >
            <AccordionItem value="overview">
              <AccordionTrigger className="text-base font-semibold text-gray-900 hover:no-underline">
                What you will see on this page
              </AccordionTrigger>
              <AccordionContent>
                <ul className="list-disc space-y-2 pl-5 text-[15px] leading-relaxed text-gray-700">
                  <li>
                    <strong className="font-medium text-gray-900">Top:</strong>{" "}
                    A search area where you can ask safety questions in plain
                    English.
                  </li>
                  <li>
                    <strong className="font-medium text-gray-900">
                      Below that:
                    </strong>{" "}
                    A <em>Knowledge Graph Explorer</em>—a visual map that shows
                    how incidents connect to equipment, locations, injuries, and
                    related details.
                  </li>
                  <li>
                    You can use the question box, the map, or both. They work
                    together to give you answers and context.
                  </li>
                </ul>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="questions">
              <AccordionTrigger className="text-base font-semibold text-gray-900 hover:no-underline">
                Ask a question in your own words
              </AccordionTrigger>
              <AccordionContent>
                <ol className="list-decimal space-y-3 pl-5 text-[15px] leading-relaxed text-gray-700">
                  <li>
                    Click in the box labeled{" "}
                    <strong className="font-medium text-gray-900">
                      Natural Language Query
                    </strong>
                    .
                  </li>
                  <li>
                    Type your question the way you would ask a coworker—for
                    example, &ldquo;What equipment shows up most in near
                    misses?&rdquo;
                  </li>
                  <li>
                    Press <strong className="font-medium text-gray-900">Search</strong>{" "}
                    or the <strong className="font-medium text-gray-900">Enter</strong>{" "}
                    key on your keyboard.
                  </li>
                  <li>
                    For ideas, open the dropdown and try{" "}
                    <strong className="font-medium text-gray-900">
                      Suggested Queries
                    </strong>{" "}
                    or pick something from{" "}
                    <strong className="font-medium text-gray-900">
                      Recent Queries
                    </strong>
                    . Press{" "}
                    <strong className="font-medium text-gray-900">Escape</strong>{" "}
                    to close the list.
                  </li>
                  <li>
                    When results appear, read the short summary and the list of
                    referenced reports (they begin with{" "}
                    <strong className="font-medium text-gray-900">SER-</strong>
                    ).
                  </li>
                  <li>
                    Use{" "}
                    <strong className="font-medium text-gray-900">
                      Export to PDF
                    </strong>{" "}
                    to save what you see. Use the{" "}
                    <strong className="font-medium text-gray-900">X</strong>{" "}
                    button to close the answer and ask something new.
                  </li>
                </ol>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="explorer">
              <AccordionTrigger className="text-base font-semibold text-gray-900 hover:no-underline">
                Build the connection map (left panel)
              </AccordionTrigger>
              <AccordionContent>
                <div className="space-y-4 text-[15px] leading-relaxed text-gray-700">
                  <p>
                    The left column is titled{" "}
                    <strong className="font-medium text-gray-900">
                      KG Explorer
                    </strong>
                    . Use it to choose what appears in the map in the middle.
                  </p>
                  <div>
                    <p className="mb-2 font-medium text-gray-900">
                      Step 1 — Pick a starting point
                    </p>
                    <ul className="list-disc space-y-2 pl-5">
                      <li>
                        <strong className="font-medium text-gray-900">
                          Browse Incidents:
                        </strong>{" "}
                        open the list and select a safety report.
                      </li>
                      <li>
                        <strong className="font-medium text-gray-900">
                          Search Entities:
                        </strong>{" "}
                        choose a category if you like, type text to find a
                        label (equipment name, place, etc.), run the search, then
                        click one result to select it.
                      </li>
                    </ul>
                  </div>
                  <div>
                    <p className="mb-2 font-medium text-gray-900">
                      Step 2 — Choose how wide the map should be
                    </p>
                    <ul className="list-disc space-y-2 pl-5">
                      <li>
                        <strong className="font-medium text-gray-900">
                          Hop depth
                        </strong>{" "}
                        (<strong className="font-medium text-gray-900">1-hop</strong>{" "}
                        or <strong className="font-medium text-gray-900">2-hop</strong>
                        ): 1-hop stays closer to your selection; 2-hop shows more
                        related items further out.
                      </li>
                      <li>
                        <strong className="font-medium text-gray-900">
                          Entity type filter:
                        </strong>{" "}
                        checkboxes control which kinds of items can appear—for
                        example incidents only, or equipment and locations
                        together. Uncheck types to simplify a busy map.
                      </li>
                    </ul>
                  </div>
                  <div>
                    <p className="mb-2 font-medium text-gray-900">
                      Step 3 — Draw the map
                    </p>
                    <p>
                      Click{" "}
                      <strong className="font-medium text-gray-900">Explore</strong>
                      . If the button is inactive, select an incident or a search
                      result first. Wait a moment while the map loads.
                    </p>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="reading">
              <AccordionTrigger className="text-base font-semibold text-gray-900 hover:no-underline">
                Read the map and the summary on the right
              </AccordionTrigger>
              <AccordionContent>
                <ul className="list-disc space-y-2 pl-5 text-[15px] leading-relaxed text-gray-700">
                  <li>
                    Dots (nodes) are items; connecting lines show how they
                    relate. Match dot colors to the{" "}
                    <strong className="font-medium text-gray-900">legend</strong>{" "}
                    below the map.
                  </li>
                  <li>
                    If a yellow notice says the view was limited because the map
                    was too large, try{" "}
                    <strong className="font-medium text-gray-900">1-hop</strong>{" "}
                    or uncheck some entity types, then click Explore again.
                  </li>
                  <li>
                    The{" "}
                    <strong className="font-medium text-gray-900">
                      right-hand panel
                    </strong>{" "}
                    shows counts and details for the map you are viewing.
                  </li>
                </ul>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </DialogContent>
    </Dialog>
  );
}
