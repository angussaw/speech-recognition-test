import React from "react";

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  WithSearch,
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

console.log("Environment Variables:");
console.log("REACT_APP_INDEX_NAME:", process.env.REACT_APP_INDEX_NAME);
console.log(
  "REACT_APP_ELASTIC_PASSWORD:",
  process.env.REACT_APP_ELASTIC_PASSWORD ? "Set (not showing value)" : "Not set"
);

const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: process.env.REACT_APP_INDEX_NAME || "cv-transcriptions",
  connectionOptions: {
    headers: {
      Authorization:
        "Basic " + btoa(`elastic:${process.env.REACT_APP_ELASTIC_PASSWORD}`),
    },
    meta: false,
  },
});

const config = {
  searchQuery: {
    search_fields: {
      generated_text: { weight: 5 },
    },
    fuzziness: true,
    result_fields: {
      filename: { raw: {} },
      generated_text: {
        snippet: {
          size: 200,
          fallback: true,
        },
      },
      duration: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} },
      up_votes: { raw: {} },
      down_votes: { raw: {} },
    },
    disjunctiveFacets: ["age", "gender", "accent"],
    facets: {
      age: { type: "value" },
      gender: { type: "value" },
      accent: { type: "value" },
      duration: {
        type: "range",
        ranges: [
          { from: 0, to: 5, name: "0-5 seconds" },
          { from: 5, to: 10, name: "5-10 seconds" },
          { from: 10, name: "10+ seconds" },
        ],
      },
    },
  },

  autocompleteQuery: {
    results: {
      fuzziness: true,
      search_fields: {
        generated_text: { weight: 3 },
      },
      result_fields: {
        generated_text: {
          snippet: {
            size: 200,
            fallback: true,
          },
        },
        filename: { raw: {} },
        duration: { raw: {} },
        age: { raw: {} },
        gender: { raw: {} },
        accent: { raw: {} },
      },
    },
  },
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true,
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={
                    <SearchBox
                      autocompleteMinimumCharacters={3}
                      debounceLength={300}
                      searchAsYouType={true}
                    />
                  }
                  sideContent={
                    <div>
                      <Facet key={"1"} field={"age"} label={"age"} />
                      <Facet key={"2"} field={"accent"} label={"accent"} />
                      <Facet key={"3"} field={"gender"} label={"gender"} />
                      <Facet key={"4"} field={"duration"} label={"duration"} />
                    </div>
                  }
                  bodyContent={<Results shouldTrackClickThrough={true} />}
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
