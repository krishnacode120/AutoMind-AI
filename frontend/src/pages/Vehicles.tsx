import { useState, useRef } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { CarFront, Pencil, Plus, Save, Trash2, X } from "lucide-react";
import { useForm } from "react-hook-form";
import PageHeader from "../components/common/PageHeader";
import Loading from "../components/common/Loading";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { deleteVehicle, saveVehicle } from "../services/vehicleApi";
import { apiErrorMessage } from "../services/api";
import type { Vehicle, VehicleCreate } from "../types/vehicle";

const defaults: VehicleCreate = {
  name: "",
  manufacturer: "",
  model: "",
  year: new Date().getFullYear(),
  fuel_type: "Petrol",
  transmission: "Automatic",
  odometer: 0,
};

export default function Vehicles() {
  const query = usePrimaryVehicle();
  const [search, setSearch] = useState("");
  const cache = useQueryClient();
  const dialog = useRef<HTMLDialogElement>(null);
  const [editing, setEditing] = useState<Vehicle | null>(null);
  const [deleting, setDeleting] = useState<Vehicle | null>(null);
  const form = useForm<VehicleCreate>({ defaultValues: defaults });
  const save = useMutation({
    mutationFn: (data: VehicleCreate) => saveVehicle(data, editing?.id),
    onSuccess: async (vehicle) => {
      await cache.invalidateQueries({ queryKey: ["vehicles"] });
      query.selectVehicle(vehicle.id);
      dialog.current?.close();
    },
  });
  const remove = useMutation({
    mutationFn: deleteVehicle,
    onSuccess: async () => {
      setDeleting(null);
      await cache.invalidateQueries();
    },
  });
  function openEditor(vehicle: Vehicle | null) {
    setEditing(vehicle);
    form.reset(vehicle ?? defaults);
    save.reset();
    dialog.current?.showModal();
  }

  return (
    <div className="resource-page">
      <div className="page-toolbar">
        <PageHeader
          title="Vehicles"
          subtitle="Your garage, connected to a little more intelligence."
        />
        <button className="action-button" onClick={() => openEditor(null)}>
          <Plus size={16} />
          Add vehicle
        </button>
      </div>
      {query.isLoading && <Loading />}
      {query.isError && (
        <p role="alert">
          {apiErrorMessage(query.error)}{" "}
          <button className="action-button" onClick={() => query.refetch()}>
            Retry
          </button>
        </p>
      )}
      {query.data?.length === 0 && (
        <p className="resource-empty">No vehicles registered.</p>
      )}
      {!!query.data?.length && (
        <div className="vehicle-list-head">
          <p>
            {query.data.length} registered{" "}
            {query.data.length === 1 ? "vehicle" : "vehicles"}
          </p>
          <input
            className="vehicle-search"
            aria-label="Search vehicles"
            placeholder="Search by name, make, or model…"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>
      )}
      {!!query.data?.length &&
        !query.data.some((vehicle) =>
          `${vehicle.name} ${vehicle.manufacturer} ${vehicle.model}`
            .toLowerCase()
            .includes(search.toLowerCase()),
        ) && <p className="resource-empty">No vehicles match your search.</p>}
      <div className="data-list">
        {query.data
          ?.filter((vehicle) =>
            `${vehicle.name} ${vehicle.manufacturer} ${vehicle.model}`
              .toLowerCase()
              .includes(search.toLowerCase()),
          )
          .map((vehicle) => (
            <article
              className={
                "data-list__item " +
                (query.vehicleId === vehicle.id ? "is-selected" : "")
              }
              key={vehicle.id}
            >
              <div>
                <div className="vehicle-card-heading">
                  <span className="vehicle-card-icon">
                    <CarFront size={23} />
                  </span>
                  <strong>{vehicle.name}</strong>
                </div>
                <p>
                  {vehicle.manufacturer} {vehicle.model} &middot; {vehicle.year}
                </p>
                <p>
                  {vehicle.fuel_type} &middot; {vehicle.transmission} &middot;{" "}
                  {vehicle.odometer.toLocaleString()} km
                </p>
              </div>
              <div className="row-actions">
                <button
                  className="action-button"
                  disabled={query.vehicleId === vehicle.id}
                  onClick={() => query.selectVehicle(vehicle.id)}
                >
                  {query.vehicleId === vehicle.id ? "Selected" : "Select"}
                </button>
                <button
                  className="icon-button"
                  title={`Edit ${vehicle.name}`}
                  aria-label={`Edit ${vehicle.name}`}
                  onClick={() => openEditor(vehicle)}
                >
                  <Pencil size={16} />
                </button>
                <button
                  className="icon-button danger"
                  title={`Delete ${vehicle.name}`}
                  aria-label={`Delete ${vehicle.name}`}
                  onClick={() => {
                    remove.reset();
                    setDeleting(vehicle);
                  }}
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </article>
          ))}
      </div>
      {deleting && (
        <section className="confirmation" role="alert">
          <p>
            Delete {deleting.name} and its telemetry history? This cannot be
            undone.
          </p>
          {remove.isError && <p>{apiErrorMessage(remove.error)}</p>}
          <div className="row-actions">
            <button
              className="action-button danger"
              disabled={remove.isPending}
              onClick={() => remove.mutate(deleting.id)}
            >
              <Trash2 size={16} />
              Confirm delete
            </button>
            <button
              className="action-button"
              disabled={remove.isPending}
              onClick={() => setDeleting(null)}
            >
              Cancel
            </button>
          </div>
        </section>
      )}
      <dialog
        ref={dialog}
        className="vehicle-dialog"
        onCancel={(event) => {
          if (save.isPending) event.preventDefault();
        }}
      >
        <form onSubmit={form.handleSubmit((data) => save.mutate(data))}>
          <div className="page-toolbar">
            <h2>{editing ? "Edit vehicle" : "Add vehicle"}</h2>
            <button
              type="button"
              className="icon-button"
              aria-label="Close editor"
              disabled={save.isPending}
              onClick={() => dialog.current?.close()}
            >
              <X size={18} />
            </button>
          </div>
          <fieldset disabled={save.isPending} className="vehicle-form">
            {(["name", "manufacturer", "model"] as const).map((field) => (
              <label key={field}>
                {field === "name"
                  ? "Vehicle name"
                  : field === "model"
                    ? "Model"
                    : "Manufacturer"}
                <input
                  {...form.register(field, {
                    required: "Required",
                    validate: (value) => Boolean(value.trim()) || "Required",
                  })}
                  required
                  maxLength={100}
                />
                <span className="field-error">
                  {form.formState.errors[field]?.message}
                </span>
              </label>
            ))}
            <label>
              Year
              <input
                type="number"
                {...form.register("year", {
                  valueAsNumber: true,
                  required: true,
                })}
                required
                min={1900}
                max={new Date().getFullYear() + 1}
              />
            </label>
            <label>
              Fuel type
              <input
                {...form.register("fuel_type", { required: true })}
                list="fuel-types"
                required
                maxLength={50}
              />
              <datalist id="fuel-types">
                {["Petrol", "Diesel", "Hybrid", "Electric", "CNG"].map(
                  (fuel) => (
                    <option key={fuel}>{fuel}</option>
                  ),
                )}
              </datalist>
            </label>
            <label>
              Transmission
              <input
                {...form.register("transmission", { required: true })}
                list="transmissions"
                required
                maxLength={50}
              />
              <datalist id="transmissions">
                <option>Automatic</option>
                <option>Manual</option>
                <option>CVT</option>
              </datalist>
            </label>
            <label>
              Odometer (km)
              <input
                type="number"
                {...form.register("odometer", { valueAsNumber: true })}
                required
                min={0}
                step="0.01"
              />
            </label>
          </fieldset>
          {save.isError && (
            <p role="alert" className="field-error">
              {apiErrorMessage(save.error)}
            </p>
          )}
          <button
            className="action-button"
            type="submit"
            disabled={save.isPending}
          >
            <Save size={16} />
            {save.isPending ? "Saving..." : "Save vehicle"}
          </button>
        </form>
      </dialog>
    </div>
  );
}
