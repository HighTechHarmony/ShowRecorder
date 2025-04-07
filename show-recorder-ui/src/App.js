import React, { useEffect, useState } from "react";
import axios from "axios";
import ReactAudioPlayer from "react-audio-player";
import { useTable, useSortBy, usePagination, useGlobalFilter } from "react-table";
import "./App.css";

function App() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentFile, setCurrentFile] = useState(null); 

  // Fetch the file list from the API
  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axios.get("/api/list_shows");
        const data = response.data.shows;
        console.log("Fetched data:", data); // Log the fetched data
        setFiles(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  // Define table columns
  const columns = React.useMemo(
    () => [
      {
        id: "preview", // Unique ID for the column
        Header: "Preview",
        accessor: "preview",
        Cell: ({ row }) => {
          const fileName = row.original.filename;
          return (
            <button
              onClick={() => setCurrentFile(`/api/files/${fileName}`)} // Set the current file to play
              title="Preview"
              style={{
                background: "none",
                border: "none",
                cursor: "pointer",
              }}
            >
              🎵
            </button>
          );
        },
      },
      {
        id: "name", // Unique ID for the column
        Header: "Name",
        accessor: "name",
      },
      {
        id: "start_date", // Unique ID for the column
        Header: "Start Date",
        accessor: "start_date",
        Cell: ({ value }) => <span>{value}</span>,
        getHeaderProps: () => ({
          style: { whiteSpace: "nowrap", width: "150px" },
        }),
        getCellProps: () => ({
          style: { whiteSpace: "nowrap", width: "150px" },
        }),
      },
      {
        id: "start_time", // Unique ID for the column
        Header: "Start Time",
        accessor: "start_time",
        Cell: ({ value }) => <span>{value}</span>,
        getHeaderProps: () => ({
          style: { whiteSpace: "nowrap", width: "100px" },
        }),
        getCellProps: () => ({
          style: { whiteSpace: "nowrap", width: "100px" },
        }),
      },
      {
        id: "end_date", // Unique ID for the column
        Header: "End Date",
        accessor: "end_date",
        Cell: ({ value }) => <span>{value}</span>,
        getHeaderProps: () => ({
          style: { whiteSpace: "nowrap", width: "150px" },
        }),
        getCellProps: () => ({
          style: { whiteSpace: "nowrap", width: "150px" },
        }),
      },
      {
        id: "end_time", // Unique ID for the column
        Header: "End Time",
        accessor: "end_time",
        Cell: ({ value }) => <span>{value}</span>,
        getHeaderProps: () => ({
          style: { whiteSpace: "nowrap", width: "100px" },
        }),
        getCellProps: () => ({
          style: { whiteSpace: "nowrap", width: "100px" },
        }),
      },
      {
        id: "filename", // Unique ID for the column
        Header: "File Name",
        accessor: "filename",
      },
      {
        id: "size", // Unique ID for the column
        Header: "Size",
        accessor: "size",
      },
      {
        id: "chunk_number", // Unique ID for the column
        Header: "Chunk Number",
        accessor: "chunk_number",
      },
      {
        id: "download", // Unique ID for the column
        Header: "Download",
        accessor: "download",
        Cell: ({ row }) => {
          const fileName = row.original.filename;
          return (
            <a
              href={`/api/files/${fileName}`}
              download
              title="Download"
              style={{
                textDecoration: "none",
                fontSize: "1.2rem",
                color: "inherit",
              }}
            >
              📥
            </a>
          );
        },
      },
    ],
    []
  );

  // Prepare data for the table
  const data = React.useMemo(
    () =>
      files.map((file) => ({
        name: file.name,
        start_date: file.start_date,
        start_time: file.start_time,
        end_date: file.end_date,
        end_time: file.end_time,
        filename: file.filename,
        size: file.size,
        chunk_number: file.chunk_number,
      })),
    [files]
  );

  // Use React Table hooks
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    page, // For pagination
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setGlobalFilter, // For search
    state: { pageIndex, globalFilter },
  } = useTable({ columns, data, initialState: { pageIndex: 0 } }, useGlobalFilter, useSortBy, usePagination);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="App">
      <h1>Recorded Shows</h1>

      {/* Search/Filter Input */}
      <input
        value={globalFilter || ""}
        onChange={(e) => setGlobalFilter(e.target.value || undefined)} // Set undefined to reset the filter
        placeholder="Filter for..."
        style={{
          marginBottom: "10px",
          padding: "8px",
          width: "100%",
          maxWidth: "400px",
        }}
      />

      <table {...getTableProps()} className="file-table">
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                  {column.render("Header")}
                  <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? " 🔽"
                        : " 🔼"
                      : ""}
                  </span>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map((row) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => (
                  <td
                    {...cell.getCellProps({
                      className: `cell-${cell.column.id}`, // Add a class based on the column ID
                    })}
                  >
                    {cell.render("Cell")}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Audio Player */}
      {currentFile && (
        <div className="audio-player">
          <h2>Now Previewing</h2>
          <ReactAudioPlayer
            src={currentFile}
            controls
            autoPlay
            style={{ width: "100%" }}
          />
        </div>
      )}

      {/* Pagination Controls */}
      <div className="pagination">
        <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
          {"<<"}
        </button>
        <button onClick={() => previousPage()} disabled={!canPreviousPage}>
          {"<"}
        </button>
        <span>
          Page{" "}
          <strong>
            {pageIndex + 1} of {pageOptions.length}
          </strong>{" "}
        </span>
        <button onClick={() => nextPage()} disabled={!canNextPage}>
          {">"}
        </button>
        <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
          {">>"}
        </button>
      </div>
    </div>
  );
}

export default App;
